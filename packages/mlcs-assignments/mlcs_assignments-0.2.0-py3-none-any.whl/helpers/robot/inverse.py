from helpers.robot.arm import RobotArm
from helpers.robot.animation import JointAngles
from helpers.maths import Point

from scipy.optimize import minimize
from math import pi as π


# TODO: Untested!
def trajectory_joint_angles_for(
    robot: RobotArm,
    trajectory: list[Point],
    starting_guess: JointAngles = JointAngles(0, 0),
) -> list[JointAngles]:
    """Calculates the necessary joint angles to follow a trajectory of the given points.

    Args:
        robot: The robot arm.
        trajectory: The points to follow.
        starting_guess: The initial guess for the joint angles.

    Returns:
        The joint angles for the given trajectory.

    Example:
        ```python
        robot_arm = ... # Some robot arm with joints at (0, 0), (1, 0), and (2, 0)
        trajectory = [Point(2, 0), Point(1, 1), Point(0, 2)]
        joint_angles = trajectory_joint_angles_for(robot_arm, trajectory)
        print(joint_angles)
        # Output: [
        #  JointAngles(theta_1=0, theta_2=0),
        #  JointAngles(theta_1=pi / 2, theta_2=-pi / 2),
        #  JointAngles(theta_1=pi / 2, theta_2=0)
        # ]
        ```

        Typically, the trajectory would have much more points than in this example.
    """
    joint_angles: list[JointAngles] = []

    for target in trajectory:
        joint_angles.append(
            joint_angles_for(
                robot,
                target,
                guess=joint_angles[-1] if joint_angles else starting_guess,
            )
        )

    return joint_angles


def joint_angles_for(
    robot: RobotArm, target: Point, guess: JointAngles = JointAngles(0, 0)
) -> JointAngles:
    """Solves the inverse kinematics problem for our 2D robot arm."""

    def objective(thetas: tuple[float, float]) -> float:
        theta_1, theta_2 = thetas
        current = robot.rotate_to(theta_1, theta_2).end_effector_position()
        return (current.x - target.x) ** 2 + (current.y - target.y) ** 2

    theta_1, theta_2 = guess
    bounds = [(theta_1 - π, theta_1 + π), (theta_2 - π, theta_2 + π)]
    result = minimize(objective, guess, method="L-BFGS-B", bounds=bounds)

    return JointAngles(result.x[0], result.x[1])
