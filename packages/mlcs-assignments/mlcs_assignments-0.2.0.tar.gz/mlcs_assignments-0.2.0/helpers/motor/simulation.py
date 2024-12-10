from typing import ClassVar
from dataclasses import dataclass, KW_ONLY
from helpers.maths import Vector

import pandas as pd
import numpy as np

from plotly.subplots import make_subplots
from plotly.graph_objects import Figure, Scatter


def padded_range_for(
    data: Vector | tuple[float, float], padding: float = 0.1
) -> tuple[float, float]:
    if len(data) == 0:
        lower, upper = 0, 1
    else:
        lower, upper = min(data), max(data)
        lower, upper = min(0, lower), max(1, upper)

    delta = upper - lower

    return lower - padding * delta, upper + padding * delta


def draw_motor_housing() -> Scatter:
    theta = np.linspace(0, 2 * np.pi, 100)

    return Scatter(
        x=np.cos(theta),
        y=np.sin(theta),
        mode="lines",
        line=dict(color="blue"),
        name="Motor Housing",
        legendgroup="Motor",
    )


@dataclass(frozen=True)
class TemperatureThresholds:
    """Describes the upper and lower temperature thresholds of a motor winding.

    Attributes:
        upper: The upper temperature threshold.
        lower: The lower temperature threshold.

    Example:
        If you have a motor with a winding that melts at 100°C and cools down at 50°C, you can
        create a `TemperatureThresholds` object like this:

        ```python
        thresholds = TemperatureThresholds(upper=100, lower=50)
        ```
    """

    upper: float
    lower: float


@dataclass(frozen=True)
class SimulationResults:
    """Describes the results of a motor simulation.

    Attributes:
        t_f: The final time of the simulation.
        t: The time vector.
        theta: The angular position vector.
        theta_f: The final angular position.
        omega: The angular velocity vector.
        T: The temperature vector.
        T_predicted: The predicted temperature vector.
        u: The control signal vector.
        T_L: The load vector.
        t_range: The time range of the simulation.
        omega_range: The range of values of the angular velocity throughout the simulation.
        T_range: The range of values of the temperature throughout the simulation.
        u_range: The range of values of the control signal throughout the simulation.
        T_L_range: The range of values of the load throughout the simulation.
        thresholds: The temperature thresholds of the motor winding to display.

    Example:
        - See [`Motor.simulate`](#helpers.motor.Motor.simulate) for an example of how to create a `SimulationResults` object.
        - Once you have the results, you can display them using the [`draw`](#helpers.motor.SimulationResults.draw) method.
        - You can also save the measurements to a CSV file using the [`save_measurements_to`](#helpers.motor.SimulationResults.save_measurements_to) method.
        - In case you want to take only a part of the simulation, you can use the [`until`](#helpers.motor.SimulationResults.until) method.
    """

    t_f: float
    _: KW_ONLY
    t: Vector
    theta: Vector
    omega: Vector
    T: Vector
    T_predicted: Vector
    u: Vector
    T_L: Vector

    t_range: tuple[float, float]
    omega_range: tuple[float, float]
    T_range: tuple[float, float]
    u_range: tuple[float, float]
    T_L_range: tuple[float, float]

    show_predicted: bool
    thresholds: TemperatureThresholds | None

    MOTOR_HOUSING_TRACE: ClassVar[Scatter] = draw_motor_housing()

    @staticmethod
    def create(
        t_f: float,
        *,
        t: Vector,
        theta: Vector,
        omega: Vector,
        T: Vector,
        T_predicted: Vector,
        u: Vector,
        T_L: Vector,
        thresholds: TemperatureThresholds | None,
    ) -> "SimulationResults":
        return SimulationResults(
            t_f,
            t=t,
            theta=theta,
            omega=omega,
            T=T,
            T_predicted=T_predicted,
            u=u,
            T_L=T_L,
            t_range=padded_range_for((0, t_f)),
            omega_range=padded_range_for(omega),
            T_range=padded_range_for(T),
            u_range=padded_range_for(u),
            T_L_range=padded_range_for(T_L),
            show_predicted=bool(np.any(T_predicted)),
            thresholds=thresholds,
        )

    def until(self, step: int) -> "SimulationResults":
        """Returns a new `SimulationResults` object with the data up to the given step.

        Args:
            step: The step to take the data up to.

        Returns:
            A new `SimulationResults` object with the data up to the given step.

        Example:
            If you have a simulation with 100 steps and you want to take only the first 50 steps, you can do this:

            ```python
            results = motor.simulate(t_f=10, steps=100)
            partial_results = results.until(50)
            print(partial_results)
            # This will print the simulation results up to the 50th step.
            ```
        """
        return SimulationResults(
            self.t_f,
            t=self.t[:step],
            theta=self.theta[:step],
            omega=self.omega[:step],
            T=self.T[:step],
            T_predicted=self.T_predicted[:step],
            u=self.u[:step],
            T_L=self.T_L[:step],
            t_range=self.t_range,
            omega_range=self.omega_range,
            T_range=self.T_range,
            u_range=self.u_range,
            T_L_range=self.T_L_range,
            show_predicted=self.show_predicted,
            thresholds=self.thresholds,
        )

    def draw(self) -> Figure:
        """Draws the simulation results.

        Returns:
            A plotly figure with the simulation results.

        Example:
            ```python
            results = motor.simulate(t_f=10, steps=100)
            results.draw().show()
            # This will show a plot with the simulation results.
            ```
        """
        figure = self._create_layout()

        self._draw_motor_on(figure)
        self._draw_angular_velocity_on(figure)
        self._draw_temperature_on(figure)
        self._draw_control_signal_on(figure)
        self._draw_load_on(figure)

        return figure

    def save_measurements_to(self, path: str, /, *, noise: float = 0.1) -> None:
        """Saves the temperature measurements to a CSV file.

        Args:
            path: The file path to save the measurements to.
            noise: The standard deviation of the gaussian noise to simulate.

        Example:
            ```python
            results = motor.simulate(t_f=10, steps=100)
            results.save_measurements_to("measurements.csv", noise=0.1)
            # This will save the temperature measurements to a CSV file with some noise.
            ```

        Note:
            The CSV file will intentionally contain some useless fake data to make it feel like
            some data you would get in real life.
        """

        # We save the temperature measurements to a CSV file and simulate gaussian noise
        # with a standard deviation of `noise`. We also add some other random data to make it
        # more confusing, just line in real life.

        # Set seed for reproducibility
        np.random.seed(42)

        pd.DataFrame(
            {
                "Motor Housing Vibration Amplitude (mm)": np.abs(
                    np.random.normal(0, 0.5, len(self.t))
                )
                + np.abs(np.sin(self.t)),
                "Motor Winding Temperature (C)": self.T
                + np.random.normal(0, noise, len(self.T)),
                "Chroniton Displacement Current (A)": np.random.normal(
                    0, 0.1, len(self.t)
                ),
                "Elapsed Time (s)": self.t,
            }
        ).to_csv(path, index=False)

    def __repr__(self) -> str:
        return ""

    @property
    def theta_f(self) -> float:
        return self.theta[-1]

    def _create_layout(self) -> Figure:
        return make_subplots(
            rows=2,
            cols=3,
            column_widths=[0.4, 0.3, 0.3],
            row_heights=[0.5, 0.5],
            horizontal_spacing=0.1,
            subplot_titles=(
                "Motor State",
                "Angular Velocity",
                "Temperature",
                "Control Signal",
                "Load",
            ),
            specs=[
                [{"rowspan": 2, "type": "xy"}, {"type": "xy"}, {"type": "xy"}],
                [None, {"type": "xy"}, {"type": "xy"}],
            ],
        ).update_layout(height=750)

    def _draw_motor_on(self, figure: Figure) -> None:
        figure.add_trace(self.MOTOR_HOUSING_TRACE, row=1, col=1)
        figure.add_trace(
            Scatter(
                x=[0, np.cos(self.theta_f)],
                y=[0, np.sin(self.theta_f)],
                mode="lines+markers",
                marker=dict(size=10),
                line=dict(width=2, color="red"),
                name="Motor Indicator",
                legendgroup="Motor",
            ),
            row=1,
            col=1,
        )

        figure.update_xaxes(range=[-1.5, 1.5], row=1, col=1)

        # Ensure the aspect ratio is square
        figure.update_layout(
            xaxis=dict(scaleanchor="y", scaleratio=1),
            yaxis=dict(scaleanchor="x", scaleratio=1),
        )

    def _draw_angular_velocity_on(self, figure: Figure) -> None:
        figure.add_trace(
            Scatter(x=self.t, y=self.omega, mode="lines", name="Angular Velocity"),
            row=1,
            col=2,
        )

        figure.update_xaxes(title_text="Time (s)", row=1, col=2, range=self.t_range)
        figure.update_yaxes(
            title_text="Angular Velocity (rad/s)", row=1, col=2, range=self.omega_range
        )

    def _draw_temperature_on(self, figure: Figure) -> None:
        figure.add_trace(
            Scatter(x=self.t, y=self.T, mode="lines", name="Temperature"),
            row=1,
            col=3,
        )

        if self.show_predicted:
            figure.add_trace(
                Scatter(
                    x=self.t,
                    y=self.T_predicted,
                    mode="lines",
                    name="Predicted Temperature",
                    line=dict(dash="dash"),
                ),
                row=1,
                col=3,
            )

        if self.thresholds is not None:
            figure.add_hline(
                y=self.thresholds.upper,
                line=dict(color="red", width=1, dash="dash"),
                annotation_text="Overheating Threshold",
                annotation_position="top right",
                annotation_font=dict(size=8),
                row=1,  # pyright: ignore[reportArgumentType]
                col=3,  # pyright: ignore[reportArgumentType]
            )

            figure.add_hline(
                y=self.thresholds.lower,
                line=dict(color="green", width=1, dash="dash"),
                annotation_text="Cooling Threshold",
                annotation_position="bottom right",
                annotation_font=dict(size=8),
                row=1,  # pyright: ignore[reportArgumentType]
                col=3,  # pyright: ignore[reportArgumentType]
            )

        figure.update_xaxes(title_text="Time (s)", row=1, col=3, range=self.t_range)
        figure.update_yaxes(
            title_text="Temperature (°C)", row=1, col=3, range=self.T_range
        )

    def _draw_control_signal_on(self, figure: Figure) -> None:
        figure.add_trace(
            Scatter(x=self.t, y=self.u, mode="lines", name="Control Signal"),
            row=2,
            col=2,
        )

        figure.update_xaxes(title_text="Time (s)", row=2, col=2, range=self.t_range)
        figure.update_yaxes(
            title_text="Control Signal (A)", row=2, col=2, range=self.u_range
        )

    def _draw_load_on(self, figure: Figure) -> None:
        figure.add_trace(
            Scatter(x=self.t, y=self.T_L, mode="lines", name="Load"), row=2, col=3
        )

        figure.update_xaxes(title_text="Time (s)", row=2, col=3, range=self.t_range)
        figure.update_yaxes(title_text="Load (N)", row=2, col=3, range=self.T_L_range)
