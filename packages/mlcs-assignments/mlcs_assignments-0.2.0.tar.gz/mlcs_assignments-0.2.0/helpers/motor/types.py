from typing import Protocol


class MotorDynamics(Protocol):
    """Represents a model for the motor dynamics.

    Example:
        If you have a motor dynamics model, you can use it to calculate the angular acceleration
        of the motor at time t like this:

        ```python
        motor_dynamics = ...  # Some motor dynamics model
        motor_dynamics(0)  # Calculate the angular acceleration at time 0
        motor_dynamics(2)  # Calculate the angular acceleration at time 2

        # It is also possible that the dynamics model has internal state for performance
        # optimization. In this case, you can reset the internal state like this:
        motor_dynamics.reset()
        ```
    """

    def __call__(self, t: float, /) -> float:
        """Return the angular acceleration at time t."""
        ...

    def reset(self) -> None:
        """Reset the motor dynamics."""
        ...


class TemperatureModel(Protocol):
    """Represents a model for the temperature of the motor winding.

    Example:
        If you have a temperature model, you can use it to calculate the temperature of the motor
        winding at time t like this:

        ```python
        temperature_model = ...  # Some temperature model
        temperature_model(0)  # Calculate the temperature at time 0
        temperature_model(2)  # Calculate the temperature at time 2

        # Much like the motor dynamics model, it is possible that the temperature model has
        # internal state for performance optimization. In this case, you can reset it like this:
        temperature_model.reset()
        ```
    """

    def __call__(self, t: float, /) -> float:
        """Return the temperature of the motor winding at time t."""
        ...

    def reset(self) -> None:
        """Reset the temperature model."""
        ...


class ControlSignal(Protocol):
    """Represents a control signal for the motor.

    Example:
        If you have a control signal, you can use it to calculate the control signal at time t like
        this:

        ```python
        control_signal = ...  # Some control signal
        control_signal(0)  # Calculate the control signal at time 0
        control_signal(2)  # Calculate the control signal at time 2
        ```
    """

    def __call__(self, t: float, /) -> float:
        """Return the control signal at time t."""
        ...


class Load(Protocol):
    """Represents a load on the motor.

    Example:
        If you have a load model, you can use it to calculate the load at time t like this:

        ```python
        load = ...  # Some load model
        load(0)  # Calculate the load at time 0
        load(2)  # Calculate the load at time 2
        ```
    """

    def __call__(self, t: float, /) -> float:
        """Return the load at time t."""
        ...


class NoMotorDynamics:
    """Represents the absence of a motor dynamics model."""

    def __call__(self, t: float) -> float:
        return 0.0

    def reset(self) -> None:
        pass


class NoTemperatureModel:
    """Represents the absence of a temperature model."""

    def __call__(self, t: float) -> float:
        return 0.0

    def reset(self) -> None:
        pass


class NoControlSignal:
    """Represents a constant control signal of 0."""

    def __call__(self, t: float) -> float:
        return 0.0


class NoLoad:
    """Represents the absence of load."""

    def __call__(self, t: float) -> float:
        return 0.0
