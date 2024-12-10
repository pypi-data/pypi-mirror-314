from helpers.maths import Matrix, Vector
from helpers.ui import (
    dot_scatter,
    line_scatter,
    set_layout_for,
    surface_scatter,
    set_3d_layout_for,
    dot_scatter_3d,
    input_to_grid,
)

import numpy as np

from plotly.graph_objs import Figure, Scatter3d, Surface
from plotly.subplots import make_subplots


def subplots(figures: list[Figure], figure_height: int = 300) -> Figure:
    n = len(figures)

    figure = make_subplots(rows=n, cols=1, shared_xaxes=True, vertical_spacing=0.05)

    for i, sub_figure in enumerate(figures, 1):
        for trace in sub_figure.data:
            figure.add_trace(trace, row=i, col=1)

        # Update y-axis title for each subplot
        figure.update_yaxes(title_text=sub_figure.layout.yaxis.title.text, row=i, col=1)

    # Update the overall figure layout
    figure.update_layout(
        height=figure_height * n,
    )

    # Update x-axis title (only for the bottom subplot)
    figure.update_xaxes(title_text=figures[-1].layout.xaxis.title.text, row=n, col=1)

    return figure


def zero_plane(x: Vector, y: Vector) -> Surface:
    X, Y = input_to_grid(np.column_stack([x, y]))
    Z = np.zeros(X.shape)

    return surface_scatter(X, Y, Z, name="Zero Plane", color="black", opacity=0.1)


def plot_features(X: Matrix, y: Vector) -> None:
    """Plots the features of the motor dataset.

    In the feature matrix $X$, the columns represent the following features&#65306;
        - $x_1$: Initial temperature.
        - $x_2$: Time difference.
        - $x_3$: Motor phase (on/off).

    The label vector $y$ represents the temperature difference.

    Args:
        X: The feature matrix.
        y: The label (target) vector.

    Example:
        ```python
        X = np.array([[1, 2, 0], [2, 3, 1], [3, 4, 0], [4, 5, 1]])
        y = np.array([10, 20, 30, 40])

        plot_features(X, y)
        # This will show a plot of the features of the motor dataset.
        ```
    """
    indices = np.arange(len(X)) * 1.0

    initial_temperature_figure = set_layout_for(
        Figure(data=[line_scatter(x=indices, y=X[:, 0], name="Initial Temperature")]),
        x_title="Data Point Index",
        y_title=r"$\text{Temperature (} x_1 \text{)}$",
    )

    time_difference_figure = set_layout_for(
        Figure(
            data=[
                line_scatter(
                    x=indices, y=X[:, 1], name="Time Difference", color="orange"
                )
            ]
        ),
        x_title="Data Point Index",
        y_title=r"$\text{Time (} x_2 \text{)}$",
    )

    phase_figure = set_layout_for(
        Figure(
            data=[line_scatter(x=indices, y=X[:, 2], name="Motor Phase", color="green")]
        ),
        x_title="Data Point Index",
        y_title=r"$\text{On/Off (} x_3 \text{)}$",
    )

    temperature_difference_figure = set_layout_for(
        Figure(
            data=[
                dot_scatter(x=indices, y=y, name="Temperature Difference", color="red")
            ]
        ),
        x_title="Data Point Index",
        y_title=r"$\text{Temperature (} y \text{)}$",
    )

    subplots(
        [
            initial_temperature_figure,
            time_difference_figure,
            phase_figure,
            temperature_difference_figure,
        ]
    ).show()


def plot_features_3d(
    X: Matrix,
    y: Vector,
    *,
    additional_traces: list[Scatter3d | Surface] = [],
) -> None:
    """Plots the features of the motor dataset in 3D.

    For information on the features and labels, see [`plot_features`](exercise_2.md#helpers.motor.plot_features).

    Args:
        X: The feature matrix.
        y: The label (target) vector.
        additional_traces: Additional traces to be added to the plot.

    Example:
        ```python
        X = np.array([[1, 2, 0], [2, 3, 1], [3, 4, 0], [4, 5, 1]])
        y = np.array([10, 20, 30, 40])

        plot_features_3d(X, y)
        # This will show a 3D plot of the features of the motor dataset.
        ```
    """
    on_indices = X[:, 2] == 1

    T_0 = X[:, 0]
    d_t = X[:, 1]
    d_T = y

    set_3d_layout_for(
        Figure(
            data=[
                dot_scatter_3d(
                    x=T_0[on_indices],
                    y=d_t[on_indices],
                    z=d_T[on_indices],
                    color="red",
                    name="Motor On",
                ),
                dot_scatter_3d(
                    x=T_0[~on_indices],
                    y=d_t[~on_indices],
                    z=d_T[~on_indices],
                    color="blue",
                    name="Motor Off",
                ),
                *additional_traces,
                zero_plane(T_0, d_t),
            ]
        ),
        title="Temperature Change vs. Initial Temperature and Running Time",
        x_title="Initial Temperature",
        y_title="Running Time",
        z_title="Temperature Change",
    ).show()
