from helpers.maths import Matrix, Vector

import numpy as np


# TODO: Untested!
def system_matrices_for(
    *, Δt: float, J: float, B: float
) -> tuple[Matrix, Vector, Vector]:
    """Returns the matrices A, b, and c for the discrete-time state-space representation of the system describing
    the actuator dynamics of the second joint of a two-joint robot arm.

    Args:
        Δt: The time step of the discrete-time system.
        J: The moment of inertia of the second joint.
        B: The damping coefficient of the second joint.

    Returns:
        A tuple containing the matrices A, b, and c. In this simple case b and c are actually vectors.

    Example:
        To get the matrices A, b, and c for a discrete-time system with a time step of 0.1, a moment of inertia of 1,
        and a damping coefficient of 0.5, you can use the following code:

        ```python
        Δt = 0.1
        J = 1
        B = 0.5
        A, b, c = system_matrices_for(Δt=Δt, J=J, B=B)
        print(A)
        # Output: [[1. 0.10]
        #          [0. 0.95]]
        print(b)
        # Output: [0. 0.1]
        print(c)
        # Output: [1. 0.]
        ```
    """
    A = np.array([[1, Δt], [0, 1 - Δt * B / J]])
    b = np.array([0, Δt / J])
    c = np.array([1, 0])

    return A, b, c
