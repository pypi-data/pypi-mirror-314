from typing import Any


def basic_animation_configuration(redraw: bool = True) -> dict[str, Any]:
    return dict(
        type="buttons",
        buttons=[
            dict(
                label="Play",
                method="animate",
                args=[
                    None,
                    {
                        "frame": {"duration": 10, "redraw": redraw},
                        "fromcurrent": True,
                        "transition": {"duration": 0},
                    },
                ],
            )
        ],
    )
