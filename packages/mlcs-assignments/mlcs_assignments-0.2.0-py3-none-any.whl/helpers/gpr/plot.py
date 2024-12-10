from typing import Sequence
from helpers.maths import Vector, Matrix
from helpers.gpr.gpr import GPR
from helpers.ui import (
    dot_scatter,
    line_scatter,
    set_layout_for,
    uncertainty_area_scatter,
    dot_scatter_3d,
    surface_scatter,
    uncertainty_volume,
    set_3d_layout_for,
    input_to_grid,
)

from plotly.graph_objects import Figure, Scatter, Surface, Scatter3d

import numpy as np


def create_traces_for(
    model: GPR,
    x: Vector,
    *,
    show_mean: bool = True,
    show_samples: bool = True,
    show_variance: bool = True,
) -> list[Scatter]:
    result = model.predict(x)
    mean = result.mean
    standard_deviation = np.sqrt(result.variance)

    data: list[Scatter] = []

    for i in range(1, 4):
        data.append(
            uncertainty_area_scatter(
                x=x,
                y_lower=mean - i * standard_deviation,
                y_upper=mean + i * standard_deviation,
                name=f"Mean +/- {i} * Standard Deviation",
                visible=show_variance,
            )
        )

    data.append(line_scatter(x=x, y=mean, visible=show_mean))
    data.append(
        dot_scatter(x=model.training.x, y=model.training.y, visible=show_samples)
    )

    return data


def plot_GPR(
    model: GPR,
    x: Vector,
    *,
    additional_traces: Sequence[Scatter] = (),
    show_mean: bool = True,
    show_samples: bool = True,
    show_variance: bool = True,
) -> None:
    """Plots the output of a Gaussian Process Regression model.

    Args:
        model: The Gaussian Process Regression model.
        x: The test input vector.
        additional_traces: Additional traces to be added to the plot.
        show_mean: Whether to show the mean prediction.
        show_samples: Whether to show the training samples.
        show_variance: Whether to show the uncertainty area around the mean prediction.

    Example:
        If you want to see how a Gaussian Process Regression model behaves, you can plot it as follows:

        ```python
        model = ... # Create a GPR model.
        x = ... # Create a test input vector.

        plot_GPR(model, x)
        # This will show a plot of the GPR model's output.
        ```
    """
    data = create_traces_for(
        model,
        x,
        show_mean=show_mean,
        show_samples=show_samples,
        show_variance=show_variance,
    )

    set_layout_for(
        Figure(data=[*data, *additional_traces]),
        title=f"GPR with kernel {model.covariance_matrix} and {model.sigma_noise if model.sigma_noise else 'no'} noise",
        x_title="x",
        y_title="f(x)",
    ).show()


def create_traces_for_3d(
    model: GPR,
    x: Matrix,
    *,
    show_mean: bool = True,
    show_samples: bool = True,
    show_variance: bool = True,
) -> list[Surface | Scatter3d]:
    X, Y = input_to_grid(x)

    result = model.predict(x)
    mean = result.mean
    standard_deviation = np.sqrt(result.variance)

    data: list[Surface | Scatter3d] = []

    if show_variance:
        for i in range(1, 4):
            lower_surface, upper_surface = uncertainty_volume(
                x=X,
                y=Y,
                z_lower=(mean - i * standard_deviation).reshape(X.shape),
                z_upper=(mean + i * standard_deviation).reshape(X.shape),
                name=f"Mean +/- {i} * Standard Deviation",
                opacity=0.3 / i,
            )
            data.extend([lower_surface, upper_surface])

    if show_mean:
        data.append(
            surface_scatter(x=X, y=Y, z=mean.reshape(X.shape), name="Mean Prediction")
        )

    if show_samples:
        data.append(
            dot_scatter_3d(
                x=model.training.x[:, 0],
                y=model.training.x[:, 1],
                z=model.training.y,
                name="Training Data",
            )
        )

    return data


def plot_GPR_3d(
    model: GPR,
    x: Matrix,
    *,
    additional_traces: Sequence[Surface] = (),
    show_mean: bool = True,
    show_samples: bool = True,
    show_variance: bool = True,
) -> None:
    """Plots the output of a Gaussian Process Regression model in 3D.

    Args:
        model: The Gaussian Process Regression model.
        x: The test input matrix.
        additional_traces: Additional traces to be added to the plot.
        show_mean: Whether to show the mean prediction.
        show_samples: Whether to show the training samples.
        show_variance: Whether to show the uncertainty volume around the mean prediction.

    Example:
        If you want to see how a Gaussian Process Regression model behaves in 3D, you can plot it as follows:

        ```python
        model = ... # Create a GPR model.
        x = input_grid((-10, 10), (-10, 10), 100)

        plot_GPR_3d(model, x)
        # This will show a 3D plot of the GPR model's output.
        ```
    """
    data = create_traces_for_3d(
        model,
        x,
        show_mean=show_mean,
        show_samples=show_samples,
        show_variance=show_variance,
    )

    figure = Figure(data=[*data, *additional_traces])

    set_3d_layout_for(
        figure,
        title=f"GPR with kernel {model.covariance_matrix} and {model.sigma_noise if model.sigma_noise else 'no'} noise",
        x_title="x",
        y_title="y",
        z_title="f(x,y)",
    ).show()
