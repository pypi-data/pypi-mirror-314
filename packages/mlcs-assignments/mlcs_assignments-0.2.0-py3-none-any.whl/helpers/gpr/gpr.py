from typing import Protocol
from dataclasses import dataclass

from helpers.gpr.training import TrainingData, PredictionResults
from helpers.gpr.types import (
    CovarianceMatrixCalculator,
    Kernel,
    VectorInputKernel,
    CovarianceMatrixCalculatorWithoutKernel,
    VectorInputCovarianceMatrixCalculatorWithoutKernel,
)
from helpers.maths import Matrix, Vector


class GPR(Protocol):
    def predict(self, x: Vector) -> PredictionResults:
        """Predicts the mean and variance of the output for the given input vector x."""
        ...

    @property
    def training(self) -> TrainingData:
        """Returns the training data used by the model."""
        ...

    @property
    def covariance_matrix(self) -> CovarianceMatrixCalculator:
        """Returns the covariance matrix calculator used by the model."""
        ...

    @property
    def sigma_noise(self) -> float:
        """Returns the noise term assumed by the model."""
        ...

    @property
    def K(self) -> Matrix:
        """Returns the covariance matrix of the training data."""
        ...


class GPRCreator(Protocol):
    """This interface represents a Gaussian process regression model creator."""

    def create(
        self, training_data: TrainingData, kernel: Kernel, *, sigma_noise: float = 0
    ) -> "GPR":
        """Creates a new Gaussian process regression model.

        Args:
            training_data: The training data to use for the model.
            kernel: The kernel function to use for the model.
            sigma_noise: The noise term to assume for the model.

        Returns:
            A new Gaussian process regression model.

        Example:
            ```python
            training_data = ... # Some training data
            gpr_creator = ... # Some implementation of a GPR creator

            model = gpr_creator.create(training_data, kernel)
            # This will create a new GPR model with the given training data and kernel.
            ```

            If your GPR implementation has a static method called `create` that takes the training data and kernel as arguments,
            you can use the class itself as the `GPRCreator` implementation.
        """
        ...


class ModelCreator(Protocol):
    """This interface represents a model creator that can create a GPR model from a vector of hyperparameters.

    Example:
        ```python
        model_creator = ... # Some implementation of a model creator
        theta = np.array([1.0, 2.0, 3.0]) # Some hyperparameters

        model = model_creator(theta)
        # This will create a GPR model with the given hyperparameters.
        ```
    """

    def __call__(self, theta: Vector) -> GPR:
        """Creates a GPR model with the given hyperparameters."""
        ...


@dataclass(frozen=True)
class ScalarInputCovarianceMatrixCalculator:
    """This class creates a covariance matrix calculator for scalar input vectors.

    It will use the specified kernel and implementation for calculating the covariance matrix.
    """

    kernel: Kernel
    covariance_matrix: CovarianceMatrixCalculatorWithoutKernel

    def __call__(self, x_1: Vector, x_2: Vector) -> Matrix:
        return self.covariance_matrix(x_1, x_2, self.kernel)

    def __str__(self) -> str:
        return str(self.kernel)


@dataclass(frozen=True)
class VectorInputCovarianceMatrixCalculator:
    """This class creates a covariance matrix calculator for vector input matrices.

    It will use the specified kernel to calculate the covariance matrix.
    """

    kernel: VectorInputKernel
    covariance_matrix: VectorInputCovarianceMatrixCalculatorWithoutKernel

    def __call__(self, x_1: Matrix, x_2: Matrix) -> Matrix:
        return self.covariance_matrix(x_1, x_2, self.kernel)

    def __str__(self) -> str:
        return str(self.kernel)
