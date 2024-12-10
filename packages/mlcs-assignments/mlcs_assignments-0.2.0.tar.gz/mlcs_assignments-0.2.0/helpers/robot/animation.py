from typing import NamedTuple, Protocol, TypeVar, Generic, Iterable
from dataclasses import dataclass
from helpers.robot.arm import AnimateableRobotArm
from helpers.ui import basic_animation_configuration

import plotly.graph_objects as go


class JointAngles(NamedTuple):
    """Angles describing the configuration of a robot arm.

    Attributes:
        theta_1: The angle of the first joint.
        theta_2: The angle of the second joint.

    Example:
        This is useful for animating the robot arm at different configurations. See the
        [`animate`](helpers.robot.animation.html#helpers.robot.animation.animate) function for more details.
    """

    theta_1: float
    theta_2: float

    @staticmethod
    def combining(
        theta_1s: Iterable[float], theta_2s: Iterable[float]
    ) -> list["JointAngles"]:
        """Combines two lists of angles into a single list of `JointAngles`."

        Args:
            theta_1s: The angles of the first joint.
            theta_2s: The angles of the second joint.

        Returns:
            A list of `JointAngles` where each element is a pair of angles from the input lists.

        Example:
            ```python
            theta_1s = [pi, pi / 2, 0]
            theta_2s = [0, pi / 2, pi]
            joint_angles = JointAngles.combining(theta_1s, theta_2s)
            print(joint_angles)
            # Output: [
            #   JointAngles(theta_1=pi, theta_2=0),
            #   JointAngles(theta_1=pi / 2, theta_2=pi / 2),
            #   JointAngles(theta_1=0, theta_2=pi)
            # ]
            ```
        """
        return [
            JointAngles(theta_1, theta_2)
            for theta_1, theta_2 in zip(theta_1s, theta_2s)
        ]


RobotT = TypeVar("RobotT", infer_variance=True, bound=AnimateableRobotArm)


class AnimationFramesProvider(Protocol, Generic[RobotT]):
    def __call__(
        self, robot: RobotT, joint_angles: list[JointAngles]
    ) -> list[go.Figure]:
        """Returns the frames of the robot arm animation."""
        ...


@dataclass(frozen=True)
class RobotAnimator(Generic[RobotT]):
    animation_frames_for: AnimationFramesProvider[RobotT]

    @staticmethod
    def using(
        animation_frames_for: AnimationFramesProvider[RobotT],
    ) -> "RobotAnimator[RobotT]":
        """Creates an `Animator` with the given `animation_frames_for` function."""
        return RobotAnimator(animation_frames_for)

    def animate(
        self,
        robot: RobotT,
        joint_angles: list[JointAngles],
        *,
        align_starting_position: bool = False,
        subtitle: str = "",
    ) -> None:
        """Animates the robot arm moving through the given joint angles.

        Args:
            robot: The robot arm to animate.
            joint_angles: The joint angles to animate the robot arm through.
            align_starting_position: Whether to align the starting position of the robot arm with the first joint angle.
            subtitle: The subtitle of the animation.

        Example:
            if you want to show the robot arm moving through the configurations:

            (0, 0) -> (pi/6, 0) -> (pi/5, 0) -> (pi/4, pi/6) -> (pi/3, pi/6) -> (pi/2, pi/6)

            You can do that with the following code:

            ```python
            robot = ... # Some robot arm
            joint_angles = [
                JointAngles(0, 0),
                JointAngles(pi/6, 0),
                JointAngles(pi/5, 0),
                JointAngles(pi/4, pi/6),
                JointAngles(pi/3, pi/6),
                JointAngles(pi/2, pi/6),
            ]

            animate(robot, joint_angles)
            # This will animate the robot arm moving through the configurations.
            ```

            This animation would look quite ugly though. To make a nice smooth animation, you should use
            much more intermediate configurations (e.g. 100).
        """
        if align_starting_position:
            robot.rotate_to(*joint_angles[0])

        starting_frame = robot.draw(show=False, trace=[robot.end_effector_position()])
        figure = go.Figure(
            data=starting_frame.data,
            layout=starting_frame.layout,
            frames=[
                go.Frame(data=figure.data)
                for figure in self.animation_frames_for(robot, joint_angles)
            ],
        )

        figure.update_layout(
            title=f"Animated {robot.name} {subtitle}",
            updatemenus=[basic_animation_configuration()],
        )
        figure.show()
