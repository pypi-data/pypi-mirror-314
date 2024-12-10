from typing import Final, Protocol
from dataclasses import dataclass, field
from helpers.motor.types import ControlSignal
from helpers.motor.motor import Motor
from helpers.maths.solver import IntegratingFactors


class TemperaturePredictor(Protocol):
    def predict(self, t: float, on: bool) -> float:
        """Predicts the temperature of the motor at time `t`, considering if the motor is on or off.

        Args:
            t: The time to predict the temperature at.
            on: Whether the motor is on or off.

        Returns:
            The predicted temperature of the motor at time `t`.
        """
        ...

    def rollback(self) -> None:
        """Rolls back the most recent prediction.

        The `TemperaturePredictor` may store the most recent prediction internally, to make computing the prediction
        at the next time point faster. This method can be used to discard the most recent prediction and force the
        predictor to recompute the prediction from scratch.
        """
        ...

    def reset(self) -> None:
        """Resets the predictor to its initial state."""
        ...


class TemperatureSensor:
    """This class models the temperature dynamics of a motor winding. It's called sensor, but it's actually a model.

    Example:
        See [`TemperatureSensor.for_motor`](exercise_2.md#helpers.motor.TemperatureSensor.for_motor) for an example
        of how to create a temperature sensor. Once you have it, you can use it just like any other
        [`TemperatureModel`](exercise_2.md#helpers.motor.TemperatureModel).
    """

    solver: Final[IntegratingFactors]

    def __init__(
        self,
        *,
        C_t: float,
        R: float,
        k: float,
        T_ambient: float,
        u: ControlSignal,
        T_0: float,
    ) -> None:
        """Initializes the temperature sensor.

        Args:
            C_t: The thermal capacity of the motor winding.
            R: The electrical resistance of the motor winding.
            k: The heat transfer coefficient of the motor winding.
            T_ambient: The ambient temperature.
            u: The control signal of the motor.
            T_0: The initial temperature of the motor winding.

        Example:
            See [`TemperatureSensor.for_motor`](exercise_2.md#helpers.motor.TemperatureSensor.for_motor) for an example
            of how to create a temperature sensor.
        """
        self.solver = IntegratingFactors(
            a=k / C_t,
            g=lambda t: (u(t) ** 2 * R + k * T_ambient) / C_t,
            y_0=T_0,
        )

    def __call__(self, t: float) -> float:
        """Returns the temperature of the motor winding at time `t`."""
        return self.solver(t)

    def reset(self) -> None:
        """Can be used to "reset" the results of the sensor to its initial state."""
        self.solver.reset()

    @staticmethod
    def for_motor(
        motor: Motor,
        *,
        C_t: float = 40,  # J/°C
        R: float = 2,  # Ω
        k: float = 0.5,  # W/°C
        T_ambient: float = 25,  # °C
        T_0: float = 25,  # °C
    ) -> "TemperatureSensor":
        """Creates a temperature sensor for the given motor.

        Args:
            motor: The motor to create the temperature sensor for.
            C_t: The thermal capacity of the motor winding.
            R: The electrical resistance of the motor winding.
            k: The heat transfer coefficient of the motor winding.
            T_ambient: The ambient temperature.
            T_0: The initial temperature of the motor winding.

        Returns:
            A temperature sensor for the given motor.

        Example:
            If you have a motor, you can create a "sensor" for it like this:

            ```python
            motor = Motor("Simple motor", omega=SomeMotorDynamics())
            sensor = TemperatureSensor.for_motor(motor)

            sensor(0)  # This will return the initial temperature of the motor winding.
            sensor(200)  # This will return the temperature of the motor winding at t = 200.

            # You can also attach the sensor to the motor like this:
            motor = motor.with_temperature(sensor)
            ```
        """
        return TemperatureSensor(
            C_t=C_t, R=R, k=k, T_ambient=T_ambient, u=motor.u, T_0=T_0
        )


@dataclass(frozen=True)
class TemperaturePredictionsCache:
    """This class caches the temperature predictions of a motor winding.

    This is useful if it is necessary to calculate the temperature of the motor winding at the same time point multiple times.

    Example:
        If you already have some `TemperaturePredictor`, you can add caching to it like this:

        ```python
        predictor = SomeTemperaturePredictor()
        cached_predictor = TemperaturePredictionsCache(predictor=predictor)
        # `cached_predictor` can now be used like a normal `TemperaturePredictor`, but it will cache the results.
        ```
    """

    predictor: TemperaturePredictor
    cache: dict[float, float] = field(default_factory=dict)

    def predict(self, t: float, on: bool) -> float:
        self.cache[t] = self.predictor.predict(t, on)
        return self.cache[t]

    def rollback(self) -> None:
        self.predictor.rollback()

    def reset(self) -> None:
        self.predictor.reset()
        self.cache.clear()

    def __call__(self, t: float) -> float:
        assert t in self.cache, f"Temperature at time {t} has not been predicted yet."
        return self.cache[t]
