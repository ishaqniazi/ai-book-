"""
Forward and Inverse Kinematics Simulation Example

This script demonstrates concepts of forward and inverse kinematics for robotic arms.
It simulates how a robot calculates where its end effector will be based on joint
angles (forward kinematics) and how it determines joint angles needed to reach
a specific position (inverse kinematics).
"""

import time
import random
import math
from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum


class KinematicType(Enum):
    """Types of kinematic calculations."""
    FORWARD = "forward"
    INVERSE = "inverse"
    DIFFERENTIAL = "differential"


@dataclass
class JointState:
    """Represents the state of a joint."""
    id: str
    angle: float  # Joint angle in radians
    min_angle: float
    max_angle: float
    link_length: float  # Length of the link after this joint


@dataclass
class Pose:
    """Represents a position and orientation in 3D space."""
    position: Tuple[float, float, float]  # x, y, z
    orientation: Tuple[float, float, float]  # roll, pitch, yaw


class ForwardKinematics:
    """Calculates end effector position from joint angles."""

    def __init__(self, joints: List[JointState]):
        self.joints = joints

    def calculate_end_effector_pose(self) -> Pose:
        """Calculate the end effector pose given current joint angles."""
        # Start at origin
        x, y, z = 0.0, 0.0, 0.0

        # Accumulate transformations through each joint
        for joint in self.joints:
            # For a simple 2D planar arm (simplified for demonstration)
            # In 3D, this would involve rotation matrices
            current_angle = joint.angle

            # Add the link length in the direction of the accumulated angle
            x += joint.link_length * math.cos(current_angle)
            y += joint.link_length * math.sin(current_angle)
            # z stays the same in this 2D simplification

        return Pose(
            position=(x, y, z),
            orientation=(0.0, 0.0, sum(j.angle for j in self.joints))  # Simplified orientation
        )

    def calculate_link_positions(self) -> List[Tuple[float, float, float]]:
        """Calculate positions of all joints/links."""
        positions = [(0.0, 0.0, 0.0)]  # Start at origin
        current_angle = 0.0
        current_x, current_y, current_z = 0.0, 0.0, 0.0

        for joint in self.joints:
            current_angle += joint.angle
            current_x += joint.link_length * math.cos(current_angle)
            current_y += joint.link_length * math.sin(current_angle)
            positions.append((current_x, current_y, current_z))

        return positions


class InverseKinematics:
    """Calculates joint angles needed to reach a target position."""

    def __init__(self, joints: List[JointState]):
        self.joints = joints
        self.max_iterations = 100
        self.tolerance = 0.01

    def calculate_joint_angles(self, target: Tuple[float, float, float]) -> Optional[List[float]]:
        """
        Calculate joint angles to reach a target position using Jacobian-based method.
        This is a simplified implementation for a 2D planar arm.
        """
        # Check if target is reachable
        max_reach = sum(joint.link_length for joint in self.joints)
        target_distance = math.sqrt(target[0]**2 + target[1]**2)

        if target_distance > max_reach:
            return None  # Target is out of reach

        # Initialize with current angles or zeros
        current_angles = [joint.angle for joint in self.joints]

        # For a 2-joint planar arm, we can solve analytically
        if len(self.joints) == 2:
            return self._solve_2dof_analytical(target, current_angles)
        else:
            # For more complex arms, use numerical methods (simplified)
            return self._solve_numerical(target, current_angles)

    def _solve_2dof_analytical(self, target: Tuple[float, float, float],
                              initial_angles: List[float]) -> Optional[List[float]]:
        """Solve inverse kinematics for a 2-DOF planar arm analytically."""
        x, y = target[0], target[1]
        l1 = self.joints[0].link_length
        l2 = self.joints[1].link_length

        # Calculate distance from origin to target
        r = math.sqrt(x**2 + y**2)

        # Check if target is reachable
        if r > l1 + l2:
            return None  # Out of reach
        if r < abs(l1 - l2):
            return None  # Too close

        # Calculate elbow angle using law of cosines
        cos_theta2 = (l1**2 + l2**2 - r**2) / (2 * l1 * l2)
        cos_theta2 = max(-1, min(1, cos_theta2))  # Clamp to valid range
        theta2 = math.pi - math.acos(cos_theta2)

        # Calculate first joint angle
        k1 = l1 + l2 * math.cos(theta2)
        k2 = l2 * math.sin(theta2)
        theta1 = math.atan2(y, x) - math.atan2(k2, k1)

        # Apply joint limits
        if (self.joints[0].min_angle <= theta1 <= self.joints[0].max_angle and
            self.joints[1].min_angle <= theta2 <= self.joints[1].max_angle):
            return [theta1, theta2]
        else:
            return None  # Solution violates joint limits

    def _solve_numerical(self, target: Tuple[float, float, float],
                        initial_angles: List[float]) -> Optional[List[float]]:
        """Solve inverse kinematics using a simplified numerical approach."""
        # This is a very simplified numerical solver for demonstration
        # In practice, you'd use Jacobian transpose, pseudoinverse, or other methods
        angles = initial_angles.copy()

        for iteration in range(self.max_iterations):
            # Calculate current position with forward kinematics
            fk = ForwardKinematics([JointState(j.id, angles[i], j.min_angle, j.max_angle, j.link_length)
                                  for i, j in enumerate(self.joints)])
            current_pose = fk.calculate_end_effector_pose()
            current_pos = current_pose.position

            # Calculate error
            error = math.sqrt(sum((target[i] - current_pos[i])**2 for i in range(2)))  # 2D error

            if error < self.tolerance:
                return angles  # Success

            # Simple gradient descent approach (very simplified)
            for i in range(min(2, len(angles))):  # Only adjust first 2 joints for simplicity
                # Perturb the angle slightly to estimate gradient
                temp_angles = angles.copy()
                temp_angles[i] += 0.01

                temp_fk = ForwardKinematics([JointState(j.id, temp_angles[i], j.min_angle, j.max_angle, j.link_length)
                                           for i, j in enumerate(self.joints)])
                temp_pose = temp_fk.calculate_end_effector_pose()
                temp_pos = temp_pose.position

                # Calculate gradient
                grad = math.sqrt(sum((target[j] - temp_pos[j])**2 for j in range(2))) - error
                angles[i] -= 0.1 * grad  # Update with learning rate

                # Apply joint limits
                angles[i] = max(self.joints[i].min_angle, min(self.joints[i].max_angle, angles[i]))

        # If we didn't converge, return None
        return None


class KinematicsDemo:
    """Main demonstration class for kinematics simulation."""

    def __init__(self):
        self.joints = self._initialize_joints()
        self.forward_kin = ForwardKinematics(self.joints)
        self.inverse_kin = InverseKinematics(self.joints)
        self.demo_step = 0
        self.max_steps = 12

    def _initialize_joints(self) -> List[JointState]:
        """Initialize the joints for the robotic arm."""
        return [
            JointState(
                id="shoulder",
                angle=0.0,
                min_angle=-math.pi/2,
                max_angle=math.pi/2,
                link_length=0.5  # meters
            ),
            JointState(
                id="elbow",
                angle=0.0,
                min_angle=-math.pi/2,
                max_angle=math.pi/2,
                link_length=0.4
            ),
            JointState(
                id="wrist",
                angle=0.0,
                min_angle=-math.pi,
                max_angle=math.pi,
                link_length=0.1  # end effector
            )
        ]

    def run_kinematics_step(self) -> bool:
        """Run one step of kinematics demonstration."""
        print(f"\n--- Kinematics Step {self.demo_step + 1} ---")

        if self.demo_step % 3 == 0:
            # Demonstrate forward kinematics
            print("Demonstrating FORWARD KINEMATICS:")
            print(f"Current joint angles: {[f'{j.angle:.2f}' for j in self.joints]}")

            pose = self.forward_kin.calculate_end_effector_pose()
            print(f"End effector position: ({pose.position[0]:.2f}, {pose.position[1]:.2f}, {pose.position[2]:.2f})")

            # Show link positions
            link_positions = self.forward_kin.calculate_link_positions()
            print(f"Link positions: {[f'({p[0]:.2f}, {p[1]:.2f})' for p in link_positions]}")

        elif self.demo_step % 3 == 1:
            # Demonstrate inverse kinematics
            print("Demonstrating INVERSE KINEMATICS:")

            # Generate a random target within reach
            max_reach = sum(j.link_length for j in self.joints)
            target_radius = random.uniform(0.3, max_reach - 0.1)
            target_angle = random.uniform(0, 2 * math.pi)
            target_x = target_radius * math.cos(target_angle)
            target_y = target_radius * math.sin(target_angle)
            target = (target_x, target_y, 0.0)

            print(f"Target position: ({target_x:.2f}, {target_y:.2f}, {target_z:.2f})")

            solution = self.inverse_kin.calculate_joint_angles(target)
            if solution:
                print(f"Calculated joint angles: {[f'{a:.2f}' for a in solution]}")

                # Update joints for next forward kinematics
                for i, angle in enumerate(solution[:len(self.joints)]):
                    self.joints[i].angle = angle
            else:
                print("No solution found (target may be out of reach or violate joint limits)")

        else:
            # Show workspace analysis
            print("Analyzing ARM WORKSPACE:")

            # Calculate workspace bounds
            max_reach = sum(j.link_length for j in self.joints)
            min_reach = max(0, self.joints[0].link_length - sum(j.link_length for j in self.joints[1:]))

            print(f"Maximum reach: {max_reach:.2f}m")
            print(f"Minimum reach (to avoid self-collision): {min_reach:.2f}m")
            print(f"Workspace area: {math.pi * (max_reach**2 - min_reach**2):.2f}m²")

            # Show current position vs workspace
            current_pose = self.forward_kin.calculate_end_effector_pose()
            current_dist = math.sqrt(current_pose.position[0]**2 + current_pose.position[1]**2)
            print(f"Current end effector distance: {current_dist:.2f}m")

        self.demo_step += 1
        return self.demo_step < self.max_steps

    def run_demo(self):
        """Run the complete kinematics demonstration."""
        print("Forward and Inverse Kinematics Simulation Demo")
        print("=" * 48)
        print("Demonstrating how robots calculate end effector positions from joint angles")
        print("(forward kinematics) and determine joint angles needed to reach a position")
        print("(inverse kinematics).\n")

        print("Kinematics concepts demonstrated:")
        print("- Forward kinematics: joint angles → end effector position")
        print("- Inverse kinematics: end effector position → joint angles")
        print("- Workspace analysis and reachability\n")

        # Run the kinematics simulation
        while self.run_kinematics_step():
            time.sleep(0.5)  # Simulate processing time

        print(f"\nDemo completed after {self.demo_step} kinematics steps")

        # Final summary
        final_pose = self.forward_kin.calculate_end_effector_pose()
        print(f"\nFinal Configuration:")
        print(f"  Joint angles: {[f'{j.angle:.2f}' for j in self.joints]}")
        print(f"  End effector position: ({final_pose.position[0]:.2f}, {final_pose.position[1]:.2f}, {final_pose.position[2]:.2f})")

        max_reach = sum(j.link_length for j in self.joints)
        print(f"  Arm reach capability: {max_reach:.2f}m")


def main():
    """Main function to run the kinematics simulation."""
    demo = KinematicsDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()