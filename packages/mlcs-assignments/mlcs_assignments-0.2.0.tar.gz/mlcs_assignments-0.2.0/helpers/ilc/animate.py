from dataclasses import dataclass
from helpers.ilc.system import LiftedSystem
from helpers.ilc.plot import plot_responses
from helpers.ilc.ilc import IlcAlgorithm, LiftedSystemT
from helpers.maths import Vector
from helpers.ui import basic_animation_configuration

import plotly.graph_objects as go


def animated_ilc_frames(
    lifted_system: LiftedSystemT,
    ilc: IlcAlgorithm[LiftedSystemT],
    *,
    y_d: Vector,
    u: Vector,
    v: float,
    s: float,
    r: float,
    max_iterations: int,
    Δt: float,
) -> list[go.Figure]:
    frames: list[go.Figure] = []

    def create_frame(iteration: int, y: Vector, y_d: Vector) -> None:
        frames.append(
            plot_responses(y, y_d, Δt=Δt, subtitle=f"Iteration {iteration}", show=False)
        )

    u = ilc(
        lifted_system,
        y_d=y_d,
        u=u,
        v=v,
        s=s,
        r=r,
        max_iterations=max_iterations,
        on_iteration=create_frame,
    )

    return frames


@dataclass(frozen=True)
class IlcAnimator:
    ilc: IlcAlgorithm

    @staticmethod
    def using(ilc: IlcAlgorithm) -> "IlcAnimator":
        """Creates an `IlcAnimator` with the given `ilc` algorithm."""
        return IlcAnimator(ilc)

    def animate_ilc(
        self,
        lifted_system: LiftedSystem,
        *,
        y_d: Vector,
        u: Vector,
        v: float,
        s: float,
        r: float,
        max_iterations: int,
        Δt: float,
    ) -> None:
        """Animates the ILC algorithm for the given system and parameters.

        Args:
            lifted_system: The lifted system to use for the ILC algorithm.
            y_d: The desired output trajectory.
            u: The initial input trajectory.
            v: The disturbance weight.
            s: The input weight.
            r: The output weight.
            max_iterations: The maximum number of iterations to run the ILC algorithm.
            Δt: The time step of the system.

        Example:
            To animate the ILC algorithm for a lifted system `lifted_system` with a desired output
            trajectory `y_d` and an initial input trajectory `u`, you can use the following code:

            ```python
            u = ...  # Some initial input trajectory, like all zeros
            y_d = ...  # Some desired output trajectory
            lifted_system = ...  # The lifted system to use
            animate_ilc(lifted_system, y_d=y_d, u=u, v=0.1, s=0.1, r=0.1, max_iterations=100, Δt=0.1)
            ```

            This will animate the ILC algorithm for the given system and parameters.
        """
        frames: list[go.Figure] = animated_ilc_frames(
            lifted_system,
            self.ilc,
            y_d=y_d,
            u=u,
            v=v,
            s=s,
            r=r,
            max_iterations=max_iterations,
            Δt=Δt,
        )

        figure = go.Figure(
            data=frames[0].data,
            layout=frames[0].layout,
            frames=[go.Frame(data=figure.data) for figure in frames],
        )

        figure.update_layout(updatemenus=[basic_animation_configuration()])
        figure.show()
