from dataclasses import dataclass, field
from helpers.maths.types import Matrix

import numpy as np


# TODO: Untested!
@dataclass(frozen=True)
class MatrixPowers:
    """Simple wrapper to make calculating matrix powers more efficient.

    Example:
        See [`power`](exercise_1.md#helpers.maths.MatrixPowers.power) method for usage examples.
    """

    A: Matrix
    cache: dict[int, Matrix] = field(default_factory=dict, init=False)

    def power(self, k: int) -> Matrix:
        """Calculate the k-th power of the matrix A.

        Args:
            k: The power to calculate.

        Returns:
            The k-th power of the matrix A.

        Example:
            You can calculate the square of a matrix like this:

            ```python
            A = ... # The MatrixPowers object
            A_squared = A.power(2)
            print(A_squared)
            # The output will be the square of the matrix A.
            ```
        """
        if k not in self.cache:
            self.cache[k] = np.linalg.matrix_power(self.A, k)

        return self.cache[k]
