# pyright: reportAttributeAccessIssue=false

from dataclasses import dataclass
from helpers.maths import Vector
from helpers.gpr.gpr import GPRCreator
from helpers.gpr.types import Kernel, RBFKernelCreator
from helpers.gpr.training import TrainingData, PredictionResults
from helpers.gpr.plot import create_traces_for
from helpers.ui import label, line_scatter

import numpy as np
from plotly.graph_objects import Figure, Scatter


@dataclass(frozen=True)
class CovarianceCalculator:
    x_values: Vector
    kernel_creator: RBFKernelCreator

    def __call__(self, figure: Figure, *, l: float, sigma: float, x_2: float) -> None:
        figure.data[0].y = self.calculate(l, sigma, x_2)

        # Update the label for x_2
        line = label(x=x_2, y=self.variance(l, sigma, x_2), text="$x_2$")
        figure.data[1].x = line.x
        figure.data[1].y = line.y

    def calculate(self, l: float, sigma: float, x_2: float) -> Vector:
        kernel = self.kernel_creator(l=l, sigma=sigma)
        return np.array([kernel(x, x_2) for x in self.x_values])

    def variance(self, l: float, sigma: float, x_2: float) -> float:
        kernel = self.kernel_creator(l=l, sigma=sigma)
        return kernel(x_2, x_2)


@dataclass(frozen=True)
class RandomDrawingGenerator:
    result: PredictionResults
    x: Vector

    def __call__(self, figure: Figure) -> None:
        figure.add_trace(
            line_scatter(
                x=self.x,
                y=np.random.multivariate_normal(
                    self.result.mean, self.result.covariance
                ),
                name="random function",
                showlegend=False,
            )
        )


@dataclass
class TrainingDataUpdater:
    gpr: GPRCreator
    training_data: TrainingData
    kernel: Kernel
    x: Vector
    point_count: int = 1  # Does not work with 1 point for some reason

    def add(self, figure: Figure) -> None:
        self.point_count = min(self.point_count + 1, len(self.training_data.x))
        self.update(figure)

    def remove(self, figure: Figure) -> None:
        self.point_count = max(1, self.point_count - 1)
        self.update(figure)

    def update(self, figure: Figure) -> None:
        traces = self.traces()

        # This is very hacky, but it works for now.
        figure.data[3].y = traces[-2].y  # mean
        figure.data[4].x = traces[-1].x  # new x values
        figure.data[4].y = traces[-1].y  # new y values

        for i in range(1, 4):
            figure.data[i - 1].y = traces[i - 1].y  # uncertainty areas

    def traces(self) -> list[Scatter]:
        training_data = self.training_data.take(self.point_count)
        model = self.gpr.create(training_data, self.kernel)
        return create_traces_for(model, self.x)


@dataclass(frozen=True)
class HyperparameterUpdater:
    gpr: GPRCreator
    kernel_creator: RBFKernelCreator
    training_data: TrainingData
    x: Vector

    def __call__(self, figure: Figure, sigma: float, l: float, noise: float) -> None:
        data = self.plot(sigma, l, noise)

        for i in range(len(data)):
            figure.data[i].y = data[i].y

    def plot(self, sigma: float, l: float, noise: float) -> list[Scatter]:
        kernel = self.kernel_creator(sigma=sigma, l=l)
        model = self.gpr.create(self.training_data, kernel, sigma_noise=noise)
        return create_traces_for(model, self.x)
