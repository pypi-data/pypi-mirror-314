from typing import Callable
from helpers.maths import Vector, Matrix

import numpy as np

from plotly.graph_objs import Figure, Scatter, Surface, Scatter3d


def set_layout_for(
    figure: Figure, *, title: str = "", x_title: str = "Input", y_title: str = "Output"
) -> Figure:
    """Sets a basic layout for the given figure.

    Args:
        figure: The figure to set the layout for.
        title: The title of the figure.
        x_title: The title of the x-axis.
        y_title: The title of the y-axis.

    Returns:
        The figure with the layout set.

    Example:
        ```python
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        scatter = line_scatter(x=x, y=y, name="Sine wave", color="red")

        figure = Figure(data=[scatter])
        set_layout_for(figure, title="Sine Wave", x_title="X", y_title="Y").show()
        # This will show a plot of the sine wave with a title and axis labels.
        ```
    """
    figure.update_layout(
        height=600,
        title=title,
        xaxis_title=x_title,
        yaxis_title=y_title,
        legend=dict(yanchor="top", y=0.9, xanchor="right", x=0.95),
    )

    return figure


def line_scatter(
    x: Vector,
    y: Vector,
    *,
    name: str = "Prediction",
    color: str = "blue",
    dash: str = "solid",
    visible: bool = True,
    showlegend: bool = True,
) -> Scatter:
    """Creates a line scatter plot for the given x and y values.

    Args:
        x: The x values of the plot.
        y: The y values of the plot.
        name: The name of the plot.
        color: The color of the line.
        dash: The dash style of the line.
        visible: Whether the plot is visible or not.
        showlegend: Whether the plot is shown in the legend or not.

    Returns:
        A plotly scatter object that can be added to a figure.

    Example:
        ```python
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        scatter = line_scatter(x=x, y=y, name="Sine wave", color="red")
        Figure(data=[scatter]).show()
        # This will show a plot of the sine wave.
        ```
    """
    return Scatter(
        x=x,
        y=y,
        name=name,
        visible=visible,
        showlegend=showlegend,
        line=dict(color=color, width=2, dash=dash),
    )


def dot_scatter(
    x: Vector,
    y: Vector,
    *,
    name: str = "Observed points",
    color: str = "red",
    visible: bool = True,
    showlegend: bool = True,
) -> Scatter:
    """Creates a dot scatter plot for the given x and y values.

    Args:
        x: The x values of the plot.
        y: The y values of the plot.
        name: The name of the plot.
        color: The color of the dots.
        visible: Whether the plot is visible or not.
        showlegend: Whether the plot is shown in the legend or not.

    Returns:
        A plotly scatter object that can be added to a figure.

    Example:
        ```python
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        scatter = dot_scatter(x=x, y=y, name="Sine wave", color="red")
        Figure(data=[scatter]).show()
        # This will show a plot of the sine wave with red dots.
        ```
    """
    return Scatter(
        x=x,
        y=y,
        name=name,
        visible=visible,
        showlegend=showlegend,
        mode="markers",
        marker=dict(color=color, size=8),
    )


def uncertainty_area_scatter(
    x: Vector,
    y_upper: Vector,
    y_lower: Vector,
    *,
    name: str = "Mean +/- Standard Deviation",
    visible: bool = True,
) -> Scatter:
    """Creates an uncertainty area scatter plot for the given x, upper bound, and lower bound values.

    Args:
        x: The x values of the plot.
        y_upper: The upper bound values of the plot.
        y_lower: The lower bound values of the plot.
        name: The name of the plot.
        visible: Whether the plot is visible or not.

    Returns:
        A plotly scatter object that can be added to a figure.

    Example:
        ```python
        x = np.linspace(0, 10, 100)
        y_lower = np.sin(x) - 0.1
        y_upper = np.sin(x) + 0.1

        scatter = uncertainty_area_scatter(x=x, y_upper=y_upper, y_lower=y_lower)
        Figure(data=[scatter]).show()
        # This will show a plot of an uncertainty area around the sine wave.
        ```
    """

    # We plot the upper bound first, which corresponds to the x values
    # Then we plot the lower bound, but in reverse order, so that the area
    # between the two lines is filled.
    return Scatter(
        x=np.concatenate((x, x[::-1])),
        y=np.concatenate((y_upper, y_lower[::-1])),
        name=name,
        visible=visible,
        showlegend=True,
        fill="toself",
        fillcolor="rgba(189,195,199,0.5)",
        line=dict(color="rgba(200,200,200,0)"),
        hoverinfo="skip",
    )


def label(
    x: float,
    y: float,
    text: str,
    *,
    position: str = "top right",
    font_size: int = 16,
    color: str = "black",
) -> Scatter:
    return Scatter(
        x=[x],
        y=[y],
        mode="text+markers",
        text=[text],
        textposition=position,
        textfont=dict(size=font_size, color=color),
        showlegend=False,
    )


def set_3d_layout_for(
    figure: Figure,
    *,
    title: str,
    x_title: str = "X",
    y_title: str = "Y",
    z_title: str = "Z",
) -> Figure:
    figure.update_layout(
        height=800,
        title=title,
        scene=dict(
            xaxis_title=x_title,
            yaxis_title=y_title,
            zaxis_title=z_title,
        ),
        legend=dict(yanchor="top", y=1.05, xanchor="right", x=1.05),
    )
    return figure


def surface_scatter(
    x: Matrix,
    y: Matrix,
    z: Matrix,
    *,
    name: str = "Prediction",
    color_scale: str = "Plasma",
    opacity: float = 1.0,
    color: str | None = None,
    visible: bool = True,
    showlegend: bool = True,
    legend_only: bool = False,
) -> Surface:
    actual_colorscale = color_scale if color is None else [[0, color], [1, color]]

    return Surface(
        x=x,
        y=y,
        z=z,
        name=name,
        visible="legendonly" if legend_only else visible,
        showlegend=showlegend,
        colorscale=actual_colorscale,
        opacity=opacity,
        showscale=False,
    )


def dot_scatter_3d(
    x: Vector,
    y: Vector,
    z: Vector,
    *,
    name: str = "Observed points",
    color: str = "red",
    visible: bool = True,
    showlegend: bool = True,
) -> Scatter3d:
    """Creates a 3D dot scatter plot for the given x, y, and z values.

    Args:
        x: The x values of the plot.
        y: The y values of the plot.
        z: The z values of the plot.
        name: The name of the plot.
        color: The color of the dots.
        visible: Whether the plot is visible or not.
        showlegend: Whether the plot is shown in the legend or not.

    Returns:
        A plotly scatter object that can be added to a figure.

    Example:
        ```python
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        z = np.cos(x)

        scatter = dot_scatter_3d(x=x, y=y, z=z, name="Sine and Cosine", color="blue")
        Figure(data=[scatter]).show()
        # This will show a 3D plot of the sine and cosine functions with blue dots.
        ```
    """
    return Scatter3d(
        x=x,
        y=y,
        z=z,
        name=name,
        visible=visible,
        showlegend=showlegend,
        mode="markers",
        marker=dict(color=color, size=5),
    )


def uncertainty_volume(
    x: Matrix,
    y: Matrix,
    z_lower: Matrix,
    z_upper: Matrix,
    *,
    name: str = "Uncertainty Volume",
    opacity: float = 0.3,
    visible: bool = True,
    showlegend: bool = True,
) -> list[Surface]:
    lower_surface = Surface(
        x=x,
        y=y,
        z=z_lower,
        name=name + " (lower bound)",
        visible=visible,
        showlegend=showlegend,
        legendgroup=name,
        colorscale="Blues",
        opacity=opacity,
        showscale=False,
    )
    upper_surface = Surface(
        x=x,
        y=y,
        z=z_upper,
        name=name + " (upper bound)",
        visible=visible,
        showlegend=showlegend,
        legendgroup=name,
        colorscale="Reds",
        opacity=opacity,
        showscale=False,
    )
    return [lower_surface, upper_surface]


def input_grid(
    x_range: tuple[float, float], y_range: tuple[float, float], m: int
) -> Matrix:
    """Creates a grid of input points for a 2D function.

    Args:
        x_range: The range of x values.
        y_range: The range of y values.
        m: The number of points in the grid.

    Returns:
        A matrix of input points for the 2D function.

    Example:
        ```python
        x = input_grid((-10, 10), (-10, 10), 100)
        # This will create a grid of 100 points in the range [-10, 10] x [-10, 10].
        ```
    """
    points_per_dimension = int(np.sqrt(m))
    x_0, x_f = x_range
    y_0, y_f = y_range
    delta_x = (x_f - x_0) / points_per_dimension
    delta_y = (y_f - y_0) / points_per_dimension

    x = np.arange(x_0, x_f + delta_x, delta_x)
    y = np.arange(y_0, y_f + delta_y, delta_y)
    X, Y = np.meshgrid(x, y)

    # Flatten and stack the grid to form the matrix
    return np.column_stack([X.ravel(), Y.ravel()])


def input_to_grid(x: Matrix) -> tuple[Matrix, Matrix]:
    # Separate x and y coordinates
    x_coordinates = x[:, 0]
    y_coordinates = x[:, 1]

    # Find unique values
    x_unique = np.unique(x_coordinates)
    y_unique = np.unique(y_coordinates)

    # Create meshgrid
    X, Y = np.meshgrid(x_unique, y_unique)

    return X, Y


def output_to_grid(*, x: Vector, y: Vector, z: Vector, X: Matrix, Y: Matrix) -> Matrix:
    # Initialize Z with NaN values
    Z = np.full(X.shape, np.nan)

    # Fill in Z values where we have data
    for x_k, y_k, z_k in zip(x, y, z):
        i = np.where(X[0, :] == x_k)[0][0]
        j = np.where(Y[:, 0] == y_k)[0][0]
        Z[j, i] = z_k

    return Z


def create_surface(
    x: Matrix,
    f: Callable[[Matrix], Vector],
    *,
    name: str,
    color: str,
    opacity: float,
    legend_only: bool = False,
) -> Surface:
    """Creates a surface plot for the given function f.

    Args:
        x: The input values for the function f.
        f: The function to plot.
        name: The name of the plot.
        color: The color of the surface.
        opacity: The opacity of the surface.
        legend_only: Whether the plot is only shown in the legend.

    Returns:
        A plotly surface object that can be added to a figure.

    Example:
        ```python
        x = input_grid((-10, 10), (-10, 10), 100)
        f = lambda x: np.sin(x[:, 0]) * np.cos(x[:, 1])

        surface = create_surface(x, f, name="Sine * Cosine", color="blue", opacity=0.5)
        Figure(data=[surface]).show()
        # This will show a surface plot of the product of sine and cosine.
        ```
    """
    X, Y = input_to_grid(x)
    Z = f(x).reshape(X.shape)

    return surface_scatter(
        x=X, y=Y, z=Z, name=name, color=color, opacity=opacity, legend_only=legend_only
    )
