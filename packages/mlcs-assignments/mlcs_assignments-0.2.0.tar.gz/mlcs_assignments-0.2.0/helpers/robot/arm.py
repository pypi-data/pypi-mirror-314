from typing import Protocol, Callable, TypeAlias, TypeVar, Sequence
from helpers.maths import Point

import plotly.graph_objects as go

JointPositionsFunction: TypeAlias = Callable[["RobotArm"], list["Point"]]


class RobotArm(Protocol):
    theta_1: float
    """Angle of the first joint of the robot arm."""

    theta_2: float
    """Angle of the second joint of the robot arm."""

    rotations: int
    """Number of rotations that have been made by the robot arm."""

    def joint_positions(self) -> list[Point]:
        """Returns the positions of the joints of the robot arm."""
        ...

    def end_effector_position(self) -> Point:
        """Returns the position of the end effector of the robot arm."""
        ...

    def rotate_to(self, theta_1: float, theta_2: float) -> "RobotArm":
        """Rotates the robot arm to the given angles."""
        ...

    def max_length(self) -> float:
        """Returns the maximum length of the robot arm."""
        ...

    @property
    def l_1(self) -> float:
        """Length of the first segment of the robot arm."""
        ...

    @property
    def l_2(self) -> float:
        """Length of the second segment of the robot arm."""
        ...


class AnimateableRobotArm(RobotArm, Protocol):
    @property
    def name(self) -> str:
        """The name of the robot arm."""
        ...

    def draw(self, *, show: bool = True, trace: Sequence[Point] = ()) -> go.Figure:
        """Draws the robot arm in two dimensions."""
        ...

    def _title(self) -> str:
        """Returns the title of the robot arm (for the plot)."""
        ...

    def _pimp_my_robot(self) -> dict:
        """Returns the style of the robot arm."""
        ...

    def _style_trace(self) -> dict:
        """Returns the style of the trace of the end effector."""
        ...

    def _set_layout_for(self, figure: go.Figure) -> None:
        """Sets the layout for the plot of the robot arm."""
        ...


RobotArmT = TypeVar("RobotArmT", bound=RobotArm)


class RobotArmMixin:
    def end_effector_position(self: RobotArm) -> Point:
        """Returns the position of the end effector of the robot arm.

        The end effector is the last point of a serial robot arm. You can also consider it as the "hand" of the robot arm
        and it is convenient to know where it is located in space. In our case, we consider it to also be a joint of the
        robot, even though there is no link attached after it.

        Returns:
            The position of the end effector of the robot arm.

        Example:
            ```python
            robot_arm = ... # Some robot arm with joints at (0, 0), (1, 1), and (2, 2)
            end_effector_position = robot_arm.end_effector_position()
            print(end_effector_position)
            # Output: Point(x=2, y=2)
            ```
        """
        return self.joint_positions()[-1]

    def rotate_to(self: RobotArmT, theta_1: float, theta_2: float) -> RobotArmT:
        """Rotates the robot arm to the given angles.

        The angles are given in radians and they represent the rotation of the joints of the robot arm.

        Args:
            theta_1: The angle of the first joint of the robot arm.
            theta_2: The angle of the second joint of the robot arm.

        Returns:
            The robot arm after the rotation.

        Example:
            We have a robot that looks like this:

            ```plaintext
            (0, 0)          (1, 0)          (2, 0)
            ⦾ ------------ ⦾ ------------ ⦾
            ```

            And we want it to look like this:

            ```plaintext
            (0, 1)          (1, 1)
            ⦾ ------------ ⦾
            ¦
            ¦
            ¦
            ¦
            ⦾
            (0, 0)
            ```

            We can do that with the following code:

            ```python
            robot_arm = ... # Some robot arm with joints at (0, 0), (1, 0), and (2, 0)
            robot_arm = robot_arm.rotate_to(theta_1=pi/2, theta_2=-pi/2)
            print(robot_arm.end_effector_position())
            # Output: Point(x=1, y=1)
            ```
        """
        self.theta_1 = theta_1
        self.theta_2 = theta_2
        self.rotations += 1

        return self

    def max_length(self: RobotArm) -> float:
        """Returns the maximum length of the robot arm.

        Example:
            ```python
            robot_arm = ... # Some robot arm with lengths 3 and 4
            max_length = robot_arm.max_length()
            print(max_length)
            # Output: 7
            ```
        """
        return self.l_1 + self.l_2

    def draw(
        self: AnimateableRobotArm, *, show: bool = True, trace: Sequence[Point] = ()
    ) -> go.Figure:
        """Draws the robot arm in two dimensions.

        The circles represent the joints of the robot arm and the lines represent the links between the joints. The
        base of the robot arm, i.e. the first joint, is always at the origin (0, 0).

        Args:
            show: Whether to show the plot after generating it or not (True means show the plot).
            trace: A sequence of Points that trace the path of the end effector of the robot arm.

        Returns:
            The plot of the robot arm.

        Example:
            If you want to draw the robot arm and show the plot, you can do the following:

            ```python
            robot_arm = ... # Create your robot arm
            robot_arm.draw()
            # Output: A plot of the robot arm
            ```

            In case you just want to draw the robot arm without showing the plot, you can do the following:

            ```python
            robot_arm = ... # Create your robot arm
            figure = robot_arm.draw(show=False)
            # Do something with the figure
            ```
        """
        joint_positions = self.joint_positions()

        figure = go.Figure(
            go.Scatter(
                x=[point.x for point in joint_positions],
                y=[point.y for point in joint_positions],
                **self._pimp_my_robot(),
            ),
        )

        if trace:
            figure.add_trace(
                go.Scatter(
                    x=[point.x for point in trace],
                    y=[point.y for point in trace],
                    **self._style_trace(),
                ),
            )

        self._set_layout_for(figure)

        if show:
            figure.show()

        return figure  # This will come in handy later on

    def _pimp_my_robot(self: AnimateableRobotArm) -> dict:
        """You can change this method to make your robot look even cooler!"""
        return dict(
            name=self.name,
            mode="lines+markers",
            line=dict(width=2, color="black"),
            marker=dict(
                size=10,
                symbol="circle",
                color="blue",
                line=dict(width=1, color="black"),
            ),
        )

    def _style_trace(self: AnimateableRobotArm) -> dict:
        """This is just for styling the trace of the end effector."""
        return dict(
            name=f"{self.name}'s trace",
            mode="lines",
            line=dict(width=2, color="LightBlue", dash="dash"),
        )

    def _title(self: AnimateableRobotArm) -> str:
        return (
            f"{self.name}"
            if self.rotations == 0
            else (
                f"{self.name} after {self.rotations} rotation"
                if self.rotations == 1
                else f"{self.name} after {self.rotations} rotations"
            )
        )

    def _set_layout_for(self: AnimateableRobotArm, figure: go.Figure) -> None:
        figure.update_layout(
            title=f"This is {self._title()}.",
            xaxis_title="x",
            yaxis_title="y",
            yaxis_range=[
                -self.max_length() * 1.1,
                self.max_length() * 1.1,
            ],  # 1.1 gives us some padding
            yaxis=dict(
                scaleanchor="x", scaleratio=1
            ),  # Incantation to make the aspect ratio square
        )
