from typing import Protocol
from helpers.maths import Matrix, Vector, pretty_latex
from IPython.display import display, Math

import numpy as np


class LiftedSystem(Protocol):
    def response(self, u: Vector, v: Vector) -> Vector:
        """Returns the response of the lifted system to the input u and disturbance v."""
        ...

    @property
    def m(self) -> int:
        """Returns the shift between the input and output of the system."""
        ...

    @property
    def G(self) -> Matrix:
        """Returns the matrix G of the lifted system."""
        ...

    @property
    def y_0(self) -> Vector:
        """Returns the initial output of the lifted system."""
        ...


# TODO: Untested!
class LiftedSystemMixin:
    def response_to(
        self: LiftedSystem, u: Vector, v: Vector | None = None, shift: bool = False
    ) -> Vector:
        """Returns the response of the lifted system to the input `u` and disturbance `v`.

        Args:
            u: The input to the system.
            v: The disturbance to the system.
            shift: Whether to shift the output to the right by the system's shift `m`.

        Returns:
            The response of the lifted system to the input `u` and disturbance `v`.

        Example:
            To get the response of the lifted system `lifted_system` to an input `u` and no disturbance,
            you can use the following code:

            ```python
            u = ...  # Some input to the system
            lifted_system = ... # Some lifted system
            response = lifted_system.response_to(u)
            ```

            In case you have some disturbance `v` to the system, you can use the following code:

            ```python
            u = ... # Some input to the system
            v = ... # Some disturbance to the system
            lifted_system = ... # Some lifted system
            response = lifted_system.response_to(u, v)
            ```

            The lifted system actually just captures the output of the system after the first `m` steps, since
            the output is zero before that. In case you want to compare the output of the lifted system to the
            original system, you can shift the output to the right by the system's shift `m` using the `shift`
            argument:

            ```python
            u = ... # Some input to the system
            y = ... # The actual output of the system in response to the input `u`
            lifted_system = ... # Some lifted system
            response = lifted_system.response_to(u, shift=True)

            # Now `response` and `y` will have the same length and will be correctly aligned, so you can e.g. plot them.
            plot(u, y, response)
            ```
        """

        # No disturbance is the same as a zero vector
        v = np.zeros(u.shape) if v is None else v

        # The shift here comes in handy when comparing the lifted system response to
        # the manually calculated impulse response.
        return np.concat((np.zeros(self.m if shift else 0), self.response(u, v)))

    def display(self: LiftedSystem) -> None:
        """Displays the lifted system in a readable format.

        Example:
            To display the lifted system `lifted_system`, you can use the following code:

            ```python
            lifted_system = ... # Some lifted system
            lifted_system.display()
            # Output: A LaTeX representation of the lifted system and its components
            ```
        """
        display(
            Math(
                rf"m = {self.m},\quad"
                rf"\mathbf{{G}} = {pretty_latex(self.G)},\quad"
                rf"\mathbf{{y_0}} = {pretty_latex(self.y_0)}"
            )
        )

    @property
    def N(self: LiftedSystem) -> int:
        """Returns the size of the horizon of the lifted system."""
        return self.G.shape[0]


# TODO: Untested!
def impulse(N: int) -> Vector:
    """Returns an impulse response of length `N`.

    Args:
        N: The size of the impulse response.

    Returns:
        The impulse response of length `N`.

    Example:
        To get an impulse response of length 10, you can use the following code:

        ```python
        impulse_response = impulse(10)
        print(impulse_response)
        # Output: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ```
    """
    assert N > 0, "The size of the impulse response must be greater than 0."

    impulse = np.zeros(N)
    impulse[0] = 1

    return impulse


# TODO: Untested!
def system_response_to(
    *, u: Vector, A: Matrix, b: Vector, c: Vector, x_0: Vector
) -> Vector:
    """Returns the response of the given discrete-time system to the input `u`.

    Args:
        u: The input to the system.
        A: The state transition matrix of the system.
        b: The input matrix of the system.
        c: The output matrix of the system.
        x_0: The initial state of the system.

    Returns:
        The response of the system to the input `u`.

    Example:
        ```python
        u = ...  # Some input to the system
        A = ...  # The state transition matrix of the system
        b = ...  # The input matrix of the system
        c = ...  # The output matrix of the system
        x_0 = ...  # The initial state of the system
        response = system_response_to(u=u, A=A, b=b, c=c, x_0=x_0)
        print(response)
        # Output: The response of the system to the input `u` as a vector, like [1.2, 3.4, 5.6, ...]
        ```
    """
    x = x_0
    y = []

    for u_i in u:
        y.append(c.T @ x)
        x = A @ x + b * u_i

    return np.array(y)
