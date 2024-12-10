from typing import Callable, Final
from dataclasses import dataclass, field, KW_ONLY
from scipy.integrate import quad

import numpy as np


# TODO: Untested!
@dataclass
class IntegratingFactors:
    """This class is used to solve first-order linear ordinary differential equations (ODEs) of the form:

    $y'(t) = a \\cdot y(t) + g(t),$ where $a$ is a constant, and $g(t)$ is some function of time.

    The solution to this ODE is given by:

    $y(t) = e^{-a \\cdot t} \\cdot (y_0 + \\int_{0}^{t} e^{a \\cdot \\tau} \\cdot g(\\tau) d\\tau),$
    where $y_0$ is the initial value of the function $y(t)$.

    Example:
        If $a = -1$, $g(t) = t^2 + 5$, and $y_0 = 0$, you can solve the ODE like this:

        ```python
        solver = IntegratingFactors(a=-1, g=lambda t: t ** 2 + 5, y_0=0)
        solver(0)  # This will return the initial value of the function.
        solver(10)  # This will return the value of the function at t = 10.
        ```

    Note:
        This solver is optimized for performance for the case, where the time points are given in increasing order. If you
        want to reset this internal state, you can call the [`reset`](exercise_2.md#helpers.maths.solver.IntegratingFactors.reset) method.
    """

    _: KW_ONLY
    a: Final[float]
    g: Final[Callable[[float], float]]
    y_0: Final[float]

    t_last: float = field(init=False)
    y_last: float = field(init=False)

    def __call__(self, t: float) -> float:
        assert (
            t >= self.t_last
        ), "The specified time point must be greater than or equal to the last one."

        integral = (
            self.integral_last
            + quad(lambda tau: np.exp(self.a * tau) * self.g(tau), self.t_last, t)[0]
        )
        y = np.exp(-self.a * t) * (self.y_0 + integral)

        # Don't forget to update the t and omega to be the most recent values
        self.t_last = t
        self.integral_last = integral

        return y

    def reset(self) -> None:
        """Resets the internal state of the solver."""
        self.t_last = 0
        self.integral_last = 0
