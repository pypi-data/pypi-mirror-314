from dataclasses import dataclass, KW_ONLY
from helpers.maths import Matrix, Vector


@dataclass(frozen=True)
class TrainingData:
    """This class represents the training data used by the GPR model.

    The training data consists of two vectors&#65306;
        - `x`: The input vector.
        - `y`: The output vector.

    Example:
        If you have some training data as two vectors `x` and `y`, you can create a `TrainingData` object as follows:

        ```python
        x = np.array([1, 2, 3, 4, 5])
        y = np.array([2, 4, 6, 8, 10])

        training_data = TrainingData(x=x, y=y) # This is the training data object.
        print(training_data.x) # This will print the input vector.
        print(training_data.y) # This will print the output vector.
        ```
    """

    x: Vector
    y: Vector

    def take(self, count: int) -> "TrainingData":
        """Returns new training data with only the first `count` data points.

        Args:
            count: The number of data points to keep.

        Returns:
            A new `TrainingData` object with only the first `count` data points.

        Example:
            ```python
            x = np.array([1, 2, 3, 4, 5])
            y = np.array([2, 4, 6, 8, 10])

            training_data = TrainingData(x=x, y=y)
            new_training_data = training_data.take(3)

            print(new_training_data.x) # This will print [1, 2, 3]
            print(new_training_data.y) # This will print [2, 4, 6]
            ```
        """
        return TrainingData(x=self.x[:count], y=self.y[:count])

    @property
    def m(self) -> int:
        """Returns the number of training examples."""
        return len(self.y)


@dataclass(frozen=True)
class PredictionResults:
    """This class represents the results of a prediction made by a GPR model.

    The results consist of three parts&#65306;
        - `mean`: The mean of the predicted output.
        - `covariance`: The covariance matrix of the predicted output.
        - `variance`: The variance of the predicted output (diagonal of the covariance matrix).

    Example:
        If you are creating a prediction using a GPR model, you can do so in the following way:

        ```python
        mean = ... # Some calculated mean
        covariance = ... # Some calculated covariance matrix
        variance = ... # Some calculated variance

        prediction = PredictionResults(mean=mean, covariance=covariance, variance=variance)
        print(prediction) # This will print the prediction results.
        ```

        If you have a GPR model `model` and an input vector `x`, you can make a prediction as follows:

        ```python
        prediction = model.predict(x)

        print(prediction.mean) # This will print the mean of the predicted output.
        print(prediction.covariance) # This will print the covariance matrix of the predicted output.
        print(prediction.variance) # This will print the variance of the predicted output.
        ```
    """

    _: KW_ONLY
    mean: Vector
    covariance: Matrix
    variance: Vector


@dataclass(frozen=True)
class DataSet:
    """This class represents a dataset.

    Attributes:
        X: The input matrix.
        y: The output vector.

    Example:
        If you have a dataset with input matrix `X` and output vector `y`, you can create a `DataSet` object as follows:

        ```python
        X = np.array([[1, 2], [3, 4], [5, 6]])
        y = np.array([1, 2, 3])

        dataset = DataSet(X=X, y=y) # This is the dataset object.
        print(dataset.X)  # This will print the input matrix.
        print(dataset.y)  # This will print the output vector.
        ```
    """

    X: Matrix
    y: Vector


@dataclass(frozen=True)
class DataSets:
    """This class represents a pair of training and test datasets.

    Attributes:
        training: The training dataset.
        test: The test dataset.

    Example:
        If you have a training dataset with input matrix `X_train` and output vector `y_train`,
        and a test dataset with input matrix `X_test` and output vector `y_test`, you can create a `DataSets` object as follows:

        ```python
        X_train = np.array([[1, 2], [3, 4], [5, 6]])
        y_train = np.array([1, 2, 3])

        X_test = np.array([[1, 2], [3, 4]])
        y_test = np.array([1, 2])

        data_sets = DataSets(training=DataSet(X=X_train, y=y_train), test=DataSet(X=X_test, y=y_test))
        print(data_sets.training) # This will print the training dataset.
        print(data_sets.test) # This will print the test dataset.
        ```

        You can also get the training data as a `TrainingData` object using the `training_data` method:

        ```python
        training_data = data_sets.training_data()

        print(training_data.x) # This will print the input matrix of the training data.
        print(training_data.y) # This will print the output vector of the training data.
        ```
    """

    training: DataSet
    test: DataSet

    def training_data(self) -> TrainingData:
        return TrainingData(x=self.training.X, y=self.training.y)
