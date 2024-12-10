from helpers.maths.types import Matrix, Vector
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import cg, spilu, LinearOperator

import numpy as np


def incomplete_cholesky_preconditioner(A: Matrix) -> LinearOperator:
    """Compute the Incomplete Cholesky preconditioner for matrix A."""
    A_csc = csc_matrix(A)
    ilu = spilu(A_csc, drop_tol=1e-5)

    M = LinearOperator(A.shape, ilu.solve)
    return M


# TODO: Untested!
def solve(
    A: Matrix,
    B: Vector | Matrix,
    /,
    *,
    tolerance: float = 1e-10,
    max_iterations: int | None = None,
) -> Vector | Matrix:
    """Solves AX = B for X using the Conjugate Gradient method, where A is symmetric positive definite.

    Args:
        A: The matrix A in the equation $AX = B$.
        B: The right-hand side vector or matrix in the equation $AX = B$.
        tolerance: The tolerance for the Conjugate Gradient method.
        max_iterations: The maximum number of iterations for the Conjugate Gradient method.

    Returns:
        The solution X to the equation $AX = B$.

    Example:
        If the right-hand side is just a single vector $b$, you can solve the equation like this:

        ```python
        A = np.array([[4, 1], [1, 3]])
        b = np.array([1, 2])

        x = solve(A, b)
        # Output: array([0.09090909, 0.63636364])
        ```

        You can also solve for multiple right-hand side vectors by passing a matrix as the right-hand side:

        ```python
        A = np.array([[4, 1], [1, 3]])
        B = np.array([[1, 2], [3, 4]])

        X = solve(A, B)
        # Output: array([[0.        , 0.18181818],
                         [1.        , 1.27272727]])
        ```
    """
    if not isinstance(B, np.ndarray):
        B = np.array(B)

    if A.shape[0] == 1:
        return np.array([(B / A).squeeze()])

    if B.ndim == 1:
        B = B.reshape(-1, 1)

    N, nrhs = B.shape
    solutions: list[Vector] = []

    max_iterations = max_iterations or N
    M = incomplete_cholesky_preconditioner(A)

    for i in range(nrhs):
        x, info = cg(A, B[:, i], M=M, rtol=tolerance, maxiter=max_iterations)
        if info > 0:
            # print(f"Warning: CG did not converge for column {i}. Error code: {info}")
            pass  # You can uncomment the above line if you want to see the warning

        solutions.append(x)

    # We need to transpose here, because the solution vectors are stored as rows.
    # They are expected to be columns in the result (if RHS is a matrix).
    return np.array(solutions).squeeze().T
