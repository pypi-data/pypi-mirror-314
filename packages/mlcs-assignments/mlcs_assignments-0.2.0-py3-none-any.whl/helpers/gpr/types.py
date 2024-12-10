from typing import Protocol


from helpers.maths import Matrix, Vector


class Kernel(Protocol):
    """This interface represents a kernel function that can be used to calculate the covariance matrix for a GPR model.

    Example:
        ```python
        kernel = ... # Some implementation of a kernel function
        kernel(1.0, 2.0) # This will return the value of the kernel function
                         # for x_1 = 1.0 and x_2 = 2.0, i.e. k(1.0, 2.0).
        ```
    """

    def __call__(self, x_1: float, x_2: float) -> float:
        """Computes the value of the kernel function for the two input points x_1 and x_2."""
        ...


class VectorInputKernel(Protocol):
    """This interface represents a kernel function that can be used to calculate the covariance matrix for a multi-dimensional GPR model.

    Example:
        ```python
        kernel = ... # Some implementation of a kernel function
        kernel([1.0, 2.0], [3.0, 4.0]) # This will return the value of the kernel function for x_1 = ...
                                       # ... [1.0, 2.0] and x_2 = [3.0, 4.0], i.e. k([1.0, 2.0], [3.0, 4.0]).
        ```
    """

    def __call__(self, x_1: Vector, x_2: Vector) -> float:
        """Computes the covariance matrix for the two input vectors $x_1$ and $x_2$."""
        ...


class RBFKernelCreator(Protocol):
    """This interface represents an object that can create a radial basis function kernel with a
    given length scale and standard deviation.

    Example:
        ```python
        kernel_creator = ... # Some implementation of a kernel creator
        kernel = kernel_creator(l=1.0, sigma=0.5)
        kernel # This should be a radial basis function kernel with length scale 1.0 and standard deviation 0.5.
        ```
    """

    def __call__(self, *, l: float, sigma: float) -> Kernel:
        """Creates a radial basis function kernel with length scale l and standard deviation sigma."""
        ...


class CovarianceMatrixCalculatorWithoutKernel(Protocol):
    def __call__(self, x_1: Vector, x_2: Vector, kernel: Kernel) -> Matrix:
        """Calculates the covariance matrix for the given input vectors x_1 and x_2 using the specified kernel."""
        ...


class CovarianceMatrixCalculator(Protocol):
    """This represents some object that can calculate the covariance matrix for a given set of input vectors x_1 and x_2.

    This lets use calculate the covariance matrix, without having to worry about which specific function to call, or which
    kernel to use. It is all handled by the object implementing this interface.

    Example:
        ```python
        covariance_matrix = ... # Some implementation of a covariance matrix calculator

        K = covariance_matrix(x, x)
        pretty(K)
        # This will display (some) rows of the 100x100 covariance matrix, calculated using some kernel.
        ```
    """

    def __call__(self, x_1: Vector, x_2: Vector) -> Matrix:
        """Calculates the covariance matrix for the given input vectors x_1 and x_2."""
        ...


class VectorInputCovarianceMatrixCalculatorWithoutKernel(Protocol):
    def __call__(self, x_1: Matrix, x_2: Matrix, kernel: VectorInputKernel) -> Matrix:
        """Calculates the covariance matrix for the given input matrices x_1 and x_2 using the specified kernel."""
        ...


class VectorInputCovarianceMatrixCalculator(Protocol):
    """This represents some object that can calculate the covariance matrix for a given set of input matrices x_1 and x_2.

    This lets use calculate the covariance matrix, without having to worry about which specific function to call, or which
    kernel to use. It is all handled by the object implementing this interface.

    Example:
        ```python
        covariance_matrix = ... # Some implementation of a covariance matrix calculator

        K = covariance_matrix(X, X)
        pretty(K)
        # This will display (some) rows of the 100x100 covariance matrix, calculated using some vector input kernel.
        ```
    """

    def __call__(self, x_1: Matrix, x_2: Matrix) -> Matrix:
        """Calculates the covariance matrix for the given input matrices x_1 and x_2."""
        ...
