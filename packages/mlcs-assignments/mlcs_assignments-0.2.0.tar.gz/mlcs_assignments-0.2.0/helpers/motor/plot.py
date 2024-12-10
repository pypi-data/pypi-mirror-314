from helpers.maths import Vector

from plotly.graph_objects import Figure, Scatter


def plot_temperature(*, t: Vector, T: Vector) -> Figure:
    """Plots the motor winding temperature over time.

    Args:
        t: The time vector.
        T: The temperature vector.

    Returns:
        A plotly figure that can be displayed, saved, or exported.

    Example:
        ```python
        t = linspace(0, 10, 100)
        T = linspace(20, 80, 100)

        plot_temperature(t=t, T=T).show()
        # This will show a plot of the motor winding temperature over time.
        ```
    """
    return Figure(
        data=[
            Scatter(
                x=t,
                y=T,
                mode="markers",
                name="Temperature",
                marker=dict(size=5, symbol="cross"),
            )
        ],
        layout=dict(
            title="Motor Winding Temperature",
            xaxis=dict(title="Time (s)"),
            yaxis=dict(title="Temperature (°C)"),
        ),
    )
