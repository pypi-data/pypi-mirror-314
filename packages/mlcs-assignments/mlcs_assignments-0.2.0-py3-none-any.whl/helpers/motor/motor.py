from dataclasses import dataclass, KW_ONLY, replace
from helpers.ui import basic_animation_configuration
from helpers.motor.simulation import SimulationResults, TemperatureThresholds
from helpers.motor.types import (
    MotorDynamics,
    TemperatureModel,
    ControlSignal,
    Load,
    NoMotorDynamics,
    NoTemperatureModel,
    NoControlSignal,
    NoLoad,
)

from tqdm import tqdm

import numpy as np
from plotly.graph_objects import Figure, Frame


@dataclass(frozen=True)
class Motor:
    """This is a motor model that can be simulated and animated.

    The motor model has the following components:

    - Motor dynamics: describes how the motor behaves over time.
    - Temperature model: describes how the motor's temperature changes over time.
    - Control signal: describes how the motor is controlled over time.
    - Load: describes how the motor's load changes over time.
    - Predicted temperature: describes the predicted temperature of the motor over time.

    The predicted temperature is useful, in case you want to see how a temperature prediction model
    compares to the actual temperature model.

    Attributes:
        name: The name of the motor.
        omega: The motor dynamics.
        T: The temperature model.
        u: The control signal.
        T_L: The load.
        T_predicted: The predicted temperature model.

    Example:
        - If you just want to simulate the motor dynamics, see [`simulate`](exercise_2.md#helpers.motor.Motor.simulate).
        - For animating the motor dynamics, see [`animate`](exercise_2.md#helpers.motor.Motor.animate).
    """

    name: str
    _: KW_ONLY
    omega: MotorDynamics = NoMotorDynamics()
    T: TemperatureModel = NoTemperatureModel()
    u: ControlSignal = NoControlSignal()
    T_L: Load = NoLoad()

    T_predicted: TemperatureModel = NoTemperatureModel()

    def with_dynamics(self, omega: MotorDynamics) -> "Motor":
        """Returns a new motor with the given motor dynamics."""
        return replace(self, omega=omega)

    def with_temperature(self, T: TemperatureModel) -> "Motor":
        """Returns a new motor with the given temperature model."""
        return replace(self, T=T)

    def with_control_signal(self, u: ControlSignal) -> "Motor":
        """Returns a new motor with the given control signal."""
        return replace(self, u=u)

    def with_load(self, T_L: Load) -> "Motor":
        """Returns a new motor with the given load."""
        return replace(self, T_L=T_L)

    def with_predicted_temperature(self, T_predicted: TemperatureModel) -> "Motor":
        """Returns a new motor with the given predicted temperature model."""
        return replace(self, T_predicted=T_predicted)

    def animate(
        self,
        *,
        t_f: float,
        steps: int = 100,
        thresholds: TemperatureThresholds | None = None,
    ) -> SimulationResults:
        """Animates the motor's dynamics over time.

        Args:
            t_f: The final time of the simulation.
            steps: The number of steps to simulate.
            thresholds: The temperature thresholds to show in the animation.

        Returns:
            The simulation results of the motor's dynamics.

        Example:
            ```python
            motor = Motor("Simple motor", omega=SomeMotorDynamics())
            results = motor.animate(t_f=10, steps=100)
            # This will show an animation of the motor's dynamics. It will still return the simulation results.
            ```
        """
        results = self.simulate(t_f=t_f, steps=steps, thresholds=thresholds)
        frames = create_frames(results, steps)
        starting_frame = frames[0]

        Figure(
            data=starting_frame.data,
            layout=starting_frame.layout,
            frames=[Frame(data=frame.data) for frame in frames],
        ).update_layout(
            title=f"Animated {self.name}",
            updatemenus=[basic_animation_configuration(redraw=False)],
        ).show()

        return results

    # TODO: Untested!
    def simulate(
        self, *, t_f: float, steps: int, thresholds: TemperatureThresholds | None = None
    ) -> SimulationResults:
        """Simulates the motor's dynamics over time.

        Args:
            t_f: The final time of the simulation.
            steps: The number of steps to simulate.
            thresholds: The temperature thresholds to show in the animation.

        Returns:
            The simulation results of the motor's dynamics.

        Example:
            ```python
            motor = Motor("Simple motor", omega=SomeMotorDynamics())
            results = motor.simulate(t_f=10, steps=100)
            print(results)
            # This will print the simulation results, like the motor's angular velocity, temperature, etc.
            ```
        """
        self.omega.reset()
        self.T.reset()
        self.T_predicted.reset()

        t = np.linspace(0, t_f, steps)
        theta = np.zeros(steps)
        omega = np.zeros(steps)
        T = np.zeros(steps)
        u = np.zeros(steps)
        T_L = np.zeros(steps)
        T_predicted = np.zeros(steps)

        # We do the first step manually
        omega[0] = self.omega(0)
        T[0] = self.T(0)
        u[0] = self.u(0)
        T_L[0] = self.T_L(0)
        T_predicted[0] = self.T_predicted(0)

        for i, t_i in tqdm(
            enumerate(t[1:], start=1),
            desc=f"Simulating {self.name}",
            total=steps,
            initial=1,
            unit=" time step",
        ):
            dt = t_i - t[i - 1]
            theta[i] = theta[i - 1] + omega[i - 1] * dt
            omega[i] = self.omega(t_i)
            T[i] = self.T(t_i)
            u[i] = self.u(t_i)
            T_L[i] = self.T_L(t_i)
            T_predicted[i] = self.T_predicted(t_i)

        return SimulationResults.create(
            t_f,
            t=t,
            omega=omega,
            T=T,
            T_predicted=T_predicted,
            u=u,
            T_L=T_L,
            theta=theta,
            thresholds=thresholds,
        )


def create_frames(results: SimulationResults, steps: int) -> list[Figure]:
    return [results.until(i).draw() for i in range(1, steps + 1)]
