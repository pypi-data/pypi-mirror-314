from typing import Protocol, TypeVar, Generic
from helpers.maths import Vector
from helpers.ilc.system import LiftedSystem


import numpy as np


class Disturbance(Protocol):
    """This represents a disturbance that can be applied to a system.

    Example:
        Assuming you are given a disturbance `disturbance` and an iteration `j`, you can get the disturbance
        vector like this:

        ```python
        j = ... # Some iteration
        disturbance = ... # Some disturbance
        u = ... # Some input to the system
        disturbance_at_j = disturbance(j, u)
        ```
    """

    def __call__(self, j: int, u: Vector) -> Vector:
        """Returns the disturbance at iteration j given the input u."""
        ...


class IterationCallback(Protocol):
    """This represents a callback that should be called after each iteration of the ILC algorithm.

    This is useful for monitoring the progress of the algorithm. For example, we use this to animate the
    progress of the ILC algorithm in the exercises.

    Example:
        Assuming you have a callback `callback` and an iteration `i`, you can call the callback like this:

        ```python
        i = ... # Some iteration
        y = ... # The output of the system
        y_d = ... # The desired output of the system
        callback(i, y, y_d)
        ```
    """

    def __call__(self, iteration: int, y: Vector, y_d: Vector) -> None:
        """Called after each iteration of the ILC algorithm."""
        ...


LiftedSystemT = TypeVar("LiftedSystemT", bound=LiftedSystem, infer_variance=True)


class IlcAlgorithm(Protocol, Generic[LiftedSystemT]):
    def __call__(
        self,
        lifted_system: LiftedSystemT,
        *,
        y_d: Vector,
        u: Vector,
        v: float,
        s: float,
        r: float,
        max_iterations: int,
        on_iteration: IterationCallback,
    ) -> Vector:
        """Runs the ILC algorithm on the given system."""
        ...


def no_callback(iteration: int, y: Vector, y_d: Vector) -> None:
    """Represents a callback that does nothing."""
    pass


def no_disturbance(j: int, u: Vector) -> Vector:
    """Represents a disturbance that is always zero, i.e. no disturbance."""
    return np.zeros(u.shape)
