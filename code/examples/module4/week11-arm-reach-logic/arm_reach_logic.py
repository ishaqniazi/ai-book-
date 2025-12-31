"""
Arm Reach Logic Example

This script demonstrates concepts of robotic arm reach logic and kinematics.
It simulates how a robot arm determines if it can reach a target position
and calculates the necessary joint angles to achieve the reach.
"""

import time
import random
import math
from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum


class ReachResult(Enum):
    """Results of reachability analysis."""
    REACHABLE = "reachable"
    OUT_OF_REACH = "out_of_reach"
    OBSTRUCTED = "obstructed"
    INVALID_TARGET = "invalid_target"


class JointType(Enum):
    """Types of joints in a robotic arm."""
    REVOLUTE = "revolute"  # Rotational joint
    PRISMATIC = "prismatic"  # Linear joint
    SPHERICAL = "spherical"  # Ball joint


@dataclass
class Joint:
    """Represents a joint in the robotic arm."""
    id: str
    type: JointType
    angle: float  # Current angle in radians (for revolute joints)
    position: float  # Current position (for prismatic joints)
    min_limit: float  # Minimum angle/position
    max_limit: float  # Maximum angle/position
    length: float  # Length of the link from this joint to the next


@dataclass
class ArmConfiguration:
    """Represents a configuration of the robotic arm."""
    joints: List[Joint]
    end_effector_position: Tuple[float, float, float]  # x, y, z
    end_effector_orientation: Tuple[float, float, float]  # roll, pitch, yaw


@dataclass
class Obstacle:
    """Represents an obstacle in the environment."""
    id: str
    position: Tuple[float, float, float]  # x, y, z
    size: Tuple[float, float, float]  # width, height, depth
    shape: str = "box"  # box, sphere, etc.


class SimpleArmModel:
    """Simple model of a robotic arm for reach analysis."""

    def __init__(self, base_position: Tuple[float, float, float] = (0, 0, 0)):
        self.base_position = base_position
        self.joints = self._initialize_joints()
        self.obstacles: List[Obstacle] = []
        self.max_reach = self._calculate_max_reach()

    def _initialize_joints(self) -> List[Joint]:
        """Initialize the joints of the arm."""
        return [
            Joint(
                id="base",
                type=JointType.REVOLUTE,
                angle=0.0,
                position=0.0,
                min_limit=-math.pi,
                max_limit=math.pi,
                length=0.3  # meters
            ),
            Joint(
                id="shoulder",
                type=JointType.REVOLUTE,
                angle=0.0,
                position=0.0,
                min_limit=-math.pi/2,
                max_limit=math.pi/2,
                length=0.4
            ),
            Joint(
                id="elbow",
                type=JointType.REVOLUTE,
                angle=0.0,
                position=0.0,
                min_limit=-math.pi/2,
                max_limit=math.pi/2,
                length=0.35
            ),
            Joint(
                id="wrist",
                type=JointType.REVOLUTE,
                angle=0.0,
                position=0.0,
                min_limit=-math.pi,
                max_limit=math.pi,
                length=0.15  # End effector
            )
        ]

    def _calculate_max_reach(self) -> float:
        """Calculate the maximum reach of the arm."""
        return sum(joint.length for joint in self.joints)

    def add_obstacle(self, obstacle: Obstacle):
        """Add an obstacle to the environment."""
        self.obstacles.append(obstacle)

    def is_position_reachable(self, target: Tuple[float, float, float]) -> ReachResult:
        """Check if a target position is reachable by the arm."""
        # Calculate distance from base to target
        dx = target[0] - self.base_position[0]
        dy = target[1] - self.base_position[1]
        dz = target[2] - self.base_position[2]
        distance = math.sqrt(dx*dx + dy*dy + dz*dz)

        # Check if target is within max reach
        if distance > self.max_reach:
            return ReachResult.OUT_OF_REACH

        # Check if target is too close to base (within first joint)
        if distance < 0.1:  # Minimum reach
            return ReachResult.INVALID_TARGET

        # Check for obstacles in the path
        if self._check_path_obstructed(self.base_position, target):
            return ReachResult.OBSTRUCTED

        return ReachResult.REACHABLE

    def _check_path_obstructed(self, start: Tuple[float, float, float],
                              end: Tuple[float, float, float]) -> bool:
        """Check if the path between two points is obstructed by obstacles."""
        # Simple check: see if the straight line intersects any obstacles
        for obstacle in self.obstacles:
            if self._line_intersects_box(start, end, obstacle):
                return True
        return False

    def _line_intersects_box(self, start: Tuple[float, float, float],
                            end: Tuple[float, float, float],
                            obstacle: Obstacle) -> bool:
        """Check if a line intersects with a box-shaped obstacle."""
        # Simple implementation: check if the line passes near the obstacle
        obstacle_center = obstacle.position
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        dz = end[2] - start[2]

        # Calculate the closest point on the line to the obstacle center
        # This is a simplified version - a full implementation would be more complex
        line_length_sq = dx*dx + dy*dy + dz*dz
        if line_length_sq == 0:
            return False  # Line is actually a point

        t = ((obstacle_center[0] - start[0]) * dx +
             (obstacle_center[1] - start[1]) * dy +
             (obstacle_center[2] - start[2]) * dz) / line_length_sq

        # Clamp t to [0, 1] to get the closest point on the line segment
        t = max(0, min(1, t))

        closest_point = (
            start[0] + t * dx,
            start[1] + t * dy,
            start[2] + t * dz
        )

        # Check if the closest point is within the obstacle
        dist_sq = ((closest_point[0] - obstacle_center[0])**2 +
                   (closest_point[1] - obstacle_center[1])**2 +
                   (closest_point[2] - obstacle_center[2])**2)

        # Simple check using bounding box
        half_size = (obstacle.size[0]/2, obstacle.size[1]/2, obstacle.size[2]/2)
        max_dist = math.sqrt(half_size[0]**2 + half_size[1]**2 + half_size[2]**2)

        return dist_sq <= max_dist**2

    def calculate_reach_angles(self, target: Tuple[float, float, float]) -> Optional[List[float]]:
        """Calculate joint angles to reach a target position (simplified inverse kinematics)."""
        result = self.is_position_reachable(target)
        if result != ReachResult.REACHABLE:
            return None

        # Simplified inverse kinematics for a 3-DOF arm in 2D plane
        # Project to 2D for simplicity (x-z plane)
        dx = target[0] - self.base_position[0]
        dz = target[2] - self.base_position[2]
        distance_2d = math.sqrt(dx*dx + dz*dz)

        # Height difference
        dy = target[1] - self.base_position[1]

        # Calculate angles using geometric approach
        # Link lengths (simplified as first 3 joints)
        l1 = self.joints[1].length  # shoulder
        l2 = self.joints[2].length  # elbow

        # Calculate distance from shoulder to target
        shoulder_to_target = math.sqrt(distance_2d**2 + dy**2)

        # Check if target is reachable
        if shoulder_to_target > l1 + l2:
            return None  # Target too far

        if shoulder_to_target < abs(l1 - l2):
            return None  # Target too close

        # Calculate elbow angle using law of cosines
        cos_elbow = (l1**2 + l2**2 - shoulder_to_target**2) / (2 * l1 * l2)
        elbow_angle = math.pi - math.acos(max(-1, min(1, cos_elbow)))

        # Calculate shoulder angle
        k1 = l1 + l2 * math.cos(math.pi - elbow_angle)
        k2 = l2 * math.sin(math.pi - elbow_angle)
        shoulder_angle = math.atan2(dy, distance_2d) - math.atan2(k2, k1)

        # Calculate base rotation to face target
        base_angle = math.atan2(dx, dz)

        return [base_angle, shoulder_angle, elbow_angle, 0.0]  # Last joint (wrist) angle = 0

    def get_workspace_bounds(self) -> Tuple[float, float, float, float, float, float]:
        """Get the approximate workspace bounds of the arm."""
        min_x = self.base_position[0] - self.max_reach
        max_x = self.base_position[0] + self.max_reach
        min_y = self.base_position[1] - self.max_reach
        max_y = self.base_position[1] + self.max_reach
        min_z = self.base_position[2] - self.max_reach
        max_z = self.base_position[2] + self.max_reach

        return min_x, max_x, min_y, max_y, min_z, max_z


class ReachLogicDemo:
    """Main demonstration class for arm reach logic."""

    def __init__(self):
        self.arm = SimpleArmModel()
        self.demo_step = 0
        self.max_steps = 10

    def add_environment_obstacles(self):
        """Add some obstacles to the environment."""
        # Add a table
        table = Obstacle(
            id="table",
            position=(1.0, 0.0, 0.0),
            size=(0.8, 0.8, 0.8),
            shape="box"
        )
        self.arm.add_obstacle(table)

        # Add a wall
        wall = Obstacle(
            id="wall",
            position=(0.0, 0.5, 1.5),
            size=(2.0, 1.0, 0.1),
            shape="box"
        )
        self.arm.add_obstacle(wall)

    def run_reach_analysis_step(self) -> bool:
        """Run one step of reach analysis."""
        print(f"\n--- Reach Analysis Step {self.demo_step + 1} ---")

        if self.demo_step == 0:
            print("Setting up the robotic arm environment...")
            self.add_environment_obstacles()
            print(f"Arm initialized with max reach: {self.arm.max_reach:.2f}m")
            print(f"Workspace bounds: {self.arm.get_workspace_bounds()}")

        # Generate a random target position
        target_x = random.uniform(-1.0, 1.5)
        target_y = random.uniform(0.0, 1.0)
        target_z = random.uniform(-1.0, 1.5)
        target = (target_x, target_y, target_z)

        print(f"Target position: ({target_x:.2f}, {target_y:.2f}, {target_z:.2f})")

        # Check reachability
        result = self.arm.is_position_reachable(target)
        print(f"Reachability result: {result.value}")

        if result == ReachResult.REACHABLE:
            angles = self.arm.calculate_reach_angles(target)
            if angles:
                print(f"Calculated joint angles: {[f'{a:.2f}' for a in angles]}")
            else:
                print("Could not calculate angles (IK solution not found)")

        # Show some statistics
        print(f"Base position: {self.arm.base_position}")
        print(f"Number of obstacles: {len(self.arm.obstacles)}")

        self.demo_step += 1
        return self.demo_step < self.max_steps

    def run_demo(self):
        """Run the complete arm reach logic demonstration."""
        print("Arm Reach Logic Simulation Demo")
        print("=" * 30)
        print("Simulating how a robot arm determines if it can reach a target position")
        print("and calculates the necessary joint angles to achieve the reach.\n")

        print("The system demonstrates:")
        print("- Reachability analysis considering arm kinematics")
        print("- Obstacle detection in the path")
        print("- Simplified inverse kinematics for joint angle calculation\n")

        # Run the reach analysis simulation
        while self.run_reach_analysis_step():
            time.sleep(0.4)  # Simulate processing time

        print(f"\nDemo completed after {self.demo_step} reach analysis steps")

        # Final summary
        workspace = self.arm.get_workspace_bounds()
        print(f"\nFinal Arm Configuration:")
        print(f"  Max reach: {self.arm.max_reach:.2f}m")
        print(f"  Workspace: X({workspace[0]:.1f} to {workspace[1]:.1f}), "
              f"Y({workspace[2]:.1f} to {workspace[3]:.1f}), "
              f"Z({workspace[4]:.1f} to {workspace[5]:.1f})")
        print(f"  Obstacles in environment: {len(self.arm.obstacles)}")


def main():
    """Main function to run the arm reach logic simulation."""
    demo = ReachLogicDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()