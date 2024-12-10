from typing import Any, Callable, Protocol
from dataclasses import dataclass, KW_ONLY
from helpers.ui.plot import set_layout_for

import plotly

from plotly.graph_objs import Figure, Scatter, FigureWidget
from IPython.display import display, HTML
from ipywidgets import interact, widgets


class OnButtonClick(Protocol):
    def __call__(self, figure: Figure) -> None:
        """Updates the figure when the button is clicked."""
        ...


class OnParameterUpdate(Protocol):
    def __call__(self, figure: Figure, *args: Any, **kwargs: Any) -> None:
        """Returns the new y values for the figure."""
        ...


@dataclass(frozen=True)
class Button:
    name: str
    _: KW_ONLY
    on_click: OnButtonClick


@dataclass(frozen=True)
class Slider:
    name: str
    _: KW_ONLY
    min: float
    max: float
    step: float
    default: float
    description: str = ""


def enable_plotly_latex() -> None:
    plotly.offline.init_notebook_mode()
    display(
        HTML(
            '<script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-MML-AM_SVG"></script>'
        )
    )


def interactive_figure(
    data: list[Scatter],
    *,
    title: str,
    x_title: str,
    y_title: str,
    buttons: list[Button] = [],
    sliders: list[Slider] = [],
    on_update: OnParameterUpdate | None = None,
) -> None:
    figure = set_layout_for(
        FigureWidget(data=data),  # pyright: ignore[reportArgumentType]
        title=title,
        x_title=x_title,
        y_title=y_title,
    )

    @interact(
        **{
            param.name: widgets.FloatSlider(
                value=param.default,
                min=param.min,
                max=param.max,
                step=param.step,
                description=param.description or param.name,
                style={"description_width": "200px"},
                layout=widgets.Layout(width="35%"),
            )
            for param in sliders
        }
    )
    def update(**kwargs: Any) -> None:
        assert (
            not sliders or on_update is not None
        ), "You forgot to specify an update function (on_update)."

        if on_update is not None:
            with figure.batch_update():
                on_update(figure, **kwargs)

    def click_handler_for(button: Button) -> Callable:
        def click_handler(_) -> None:
            with figure.batch_update():
                button.on_click(figure)

        return click_handler

    button_components: list[widgets.Button] = []

    for button in buttons:
        component = widgets.Button(description=button.name)
        component.on_click(click_handler_for(button))

        button_components.append(component)

    display(widgets.VBox([figure, *button_components]))


enable_plotly_latex()
