"""
Rule-Based Navigation Example

This script demonstrates concepts of rule-based navigation systems for robots.
It simulates how a robot can navigate its environment using predefined rules
and reactive behaviors rather than complex path planning algorithms.
"""

import time
import random
import math
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
from enum import Enum


class NavigationState(Enum):
    """States for the navigation system."""
    IDLE = "idle"
    NAVIGATING = "navigating"
    OBSTACLE_DETECTED = "obstacle_detected"
    TARGET_REACHED = "target_reached"
    STUCK = "stuck"


class NavigationRuleType(Enum):
    """Types of navigation rules."""
    OBSTACLE_AVOIDANCE = "obstacle_avoidance"
    GOAL_SEEKING = "goal_seeking"
    WALL_FOLLOWING = "wall_following"
    SAFETY_CHECK = "safety_check"
    PATH_CORRECTION = "path_correction"


@dataclass
class SensorReading:
    """Represents a sensor reading."""
    sensor_type: str
    distance: float  # Distance to obstacle in meters
    angle: float  # Angle relative to robot's heading in radians
    confidence: float = 1.0


@dataclass
class NavigationRule:
    """Represents a navigation rule."""
    rule_type: NavigationRuleType
    condition: str  # Condition that triggers the rule
    action: str  # Action to take when condition is met
    priority: int  # Higher number means higher priority
    active: bool = True


@dataclass
class RobotState:
    """Represents the current state of the robot."""
    position: Tuple[float, float]  # x, y coordinates
    heading: float  # Robot's heading in radians
    velocity: Tuple[float, float]  # x, y velocity components
    target: Tuple[float, float]  # Target position
    sensors: List[SensorReading]  # Current sensor readings
    state: NavigationState = NavigationState.IDLE


class RuleBasedNavigator:
    """Implements rule-based navigation for a robot."""

    def __init__(self):
        self.rules = self._initialize_navigation_rules()
        self.current_state = RobotState(
            position=(0.0, 0.0),
            heading=0.0,
            velocity=(0.0, 0.0),
            target=(10.0, 10.0),
            sensors=[]
        )
        self.navigation_history: List[RobotState] = []
        self.stuck_counter = 0
        self.max_stuck_count = 10

    def _initialize_navigation_rules(self) -> List[NavigationRule]:
        """Initialize the navigation rules."""
        return [
            NavigationRule(
                rule_type=NavigationRuleType.SAFETY_CHECK,
                condition="any_obstacle_close",
                action="emergency_stop",
                priority=10
            ),
            NavigationRule(
                rule_type=NavigationRuleType.OBSTACLE_AVOIDANCE,
                condition="front_obstacle_close",
                action="turn_away",
                priority=9
            ),
            NavigationRule(
                rule_type=NavigationRuleType.WALL_FOLLOWING,
                condition="wall_detected_right",
                action="follow_wall_right",
                priority=7
            ),
            NavigationRule(
                rule_type=NavigationRuleType.PATH_CORRECTION,
                condition="off_course",
                action="correct_heading",
                priority=6
            ),
            NavigationRule(
                rule_type=NavigationRuleType.GOAL_SEEKING,
                condition="clear_path_to_goal",
                action="move_toward_goal",
                priority=5
            )
        ]

    def update_sensors(self, sensor_readings: List[SensorReading]):
        """Update sensor readings."""
        self.current_state.sensors = sensor_readings

    def evaluate_rules(self) -> Optional[NavigationRule]:
        """Evaluate all rules and return the highest priority active rule."""
        applicable_rules = []

        for rule in self.rules:
            if rule.active and self._check_condition(rule.condition):
                applicable_rules.append(rule)

        if applicable_rules:
            # Return the rule with highest priority
            return max(applicable_rules, key=lambda r: r.priority)

        return None

    def _check_condition(self, condition: str) -> bool:
        """Check if a condition is met."""
        if condition == "any_obstacle_close":
            return any(s.distance < 0.5 for s in self.current_state.sensors)
        elif condition == "front_obstacle_close":
            front_readings = [s for s in self.current_state.sensors if abs(s.angle) < math.pi/4]
            return any(s.distance < 0.8 for s in front_readings)
        elif condition == "wall_detected_right":
            right_readings = [s for s in self.current_state.sensors if 0 < s.angle < math.pi/2]
            return len(right_readings) > 0 and any(s.distance < 1.0 for s in right_readings)
        elif condition == "off_course":
            # Check if we're significantly off the direct path to target
            target_angle = math.atan2(
                self.current_state.target[1] - self.current_state.position[1],
                self.current_state.target[0] - self.current_state.position[0]
            )
            heading_diff = abs(target_angle - self.current_state.heading)
            return heading_diff > math.pi / 3  # More than 60 degrees off
        elif condition == "clear_path_to_goal":
            # Check if path to goal is relatively clear
            target_angle = math.atan2(
                self.current_state.target[1] - self.current_state.position[1],
                self.current_state.target[0] - self.current_state.position[0]
            )
            # Check for obstacles in the general direction of the target
            angle_diff_threshold = math.pi / 6  # 30 degrees
            relevant_readings = [
                s for s in self.current_state.sensors
                if abs(self._normalize_angle(s.angle - target_angle)) < angle_diff_threshold
                and s.distance < 2.0
            ]
            return len(relevant_readings) == 0
        else:
            return False

    def _normalize_angle(self, angle: float) -> float:
        """Normalize angle to [-π, π] range."""
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle <= -math.pi:
            angle += 2 * math.pi
        return angle

    def execute_action(self, rule: NavigationRule) -> Tuple[float, float, float]:
        """Execute the action specified by the rule and return (dx, dy, dtheta)."""
        action = rule.action

        if action == "emergency_stop":
            return 0.0, 0.0, 0.0
        elif action == "turn_away":
            # Turn away from the closest obstacle
            closest_obstacle = min(self.current_state.sensors, key=lambda s: s.distance)
            turn_direction = 1.0 if closest_obstacle.angle > 0 else -1.0
            return 0.0, 0.0, turn_direction * 0.3  # Turn in place
        elif action == "follow_wall_right":
            # Move forward while maintaining distance from right wall
            return 0.1, 0.0, -0.05  # Slight right turn while moving forward
        elif action == "correct_heading":
            # Correct heading toward target
            target_angle = math.atan2(
                self.current_state.target[1] - self.current_state.position[1],
                self.current_state.target[0] - self.current_state.position[0]
            )
            heading_diff = self._normalize_angle(target_angle - self.current_state.heading)
            return 0.2, 0.0, heading_diff * 0.1  # Move forward and adjust heading
        elif action == "move_toward_goal":
            # Move directly toward the goal
            target_angle = math.atan2(
                self.current_state.target[1] - self.current_state.position[1],
                self.current_state.target[0] - self.current_state.position[0]
            )
            return 0.3 * math.cos(target_angle), 0.3 * math.sin(target_angle), 0.0
        else:
            # Default: move forward
            return 0.1, 0.0, 0.0

    def update_navigation(self) -> NavigationState:
        """Update navigation state based on rules."""
        # Evaluate rules and execute appropriate action
        active_rule = self.evaluate_rules()

        if active_rule:
            dx, dy, dtheta = self.execute_action(active_rule)
        else:
            # Default behavior: move toward goal
            target_angle = math.atan2(
                self.current_state.target[1] - self.current_state.position[1],
                self.current_state.target[0] - self.current_state.position[0]
            )
            dx = 0.2 * math.cos(target_angle)
            dy = 0.2 * math.sin(target_angle)
            dtheta = 0.0

        # Update position and heading
        new_x = self.current_state.position[0] + dx
        new_y = self.current_state.position[1] + dy
        new_heading = self._normalize_angle(self.current_state.heading + dtheta)

        # Update robot state
        self.current_state.position = (new_x, new_y)
        self.current_state.heading = new_heading
        self.current_state.velocity = (dx, dy)

        # Check for target reached
        dist_to_target = math.sqrt(
            (new_x - self.current_state.target[0])**2 +
            (new_y - self.current_state.target[1])**2
        )

        if dist_to_target < 0.5:
            self.current_state.state = NavigationState.TARGET_REACHED
        elif dist_to_target > 20.0:  # If we're getting too far from target, we might be stuck
            self.stuck_counter += 1
            if self.stuck_counter > self.max_stuck_count:
                self.current_state.state = NavigationState.STUCK
            else:
                self.current_state.state = NavigationState.NAVIGATING
        else:
            self.current_state.state = NavigationState.NAVIGATING
            self.stuck_counter = max(0, self.stuck_counter - 1)  # Reduce stuck counter when making progress

        # Add to navigation history
        self.navigation_history.append(self.current_state)

        return self.current_state.state

    def get_navigation_status(self) -> Dict:
        """Get current navigation status."""
        dist_to_target = math.sqrt(
            (self.current_state.position[0] - self.current_state.target[0])**2 +
            (self.current_state.position[1] - self.current_state.target[1])**2
        )

        return {
            'current_position': self.current_state.position,
            'target_position': self.current_state.target,
            'distance_to_target': dist_to_target,
            'current_heading': self.current_state.heading,
            'current_velocity': self.current_state.velocity,
            'navigation_state': self.current_state.state.value,
            'active_rules_count': len([r for r in self.rules if r.active]),
            'stuck_counter': self.stuck_counter
        }


class RuleBasedNavigationDemo:
    """Main demonstration class for rule-based navigation."""

    def __init__(self):
        self.navigator = RuleBasedNavigator()
        self.demo_step = 0
        self.max_steps = 20
        self.navigation_successful = False

    def generate_simulated_sensors(self) -> List[SensorReading]:
        """Generate simulated sensor readings."""
        readings = []

        # Generate sensor readings in a circular pattern around the robot
        for angle in [i * math.pi / 8 for i in range(16)]:  # 16 sensors in 360 degrees
            # Add some randomness to simulate real-world sensor noise
            distance = random.uniform(0.5, 3.0)

            # Add some obstacles based on position to create interesting navigation scenarios
            x, y = self.navigator.current_state.position
            target_x, target_y = self.navigator.current_state.target

            # Create a "wall" between current position and target to make navigation interesting
            if abs(x - target_x) < 2.0 and abs(y - 1.0) < 0.5 and angle > -math.pi/3 and angle < math.pi/3:
                distance = 0.3  # Obstacle in the way

            readings.append(SensorReading(
                sensor_type="range",
                distance=distance,
                angle=angle,
                confidence=0.9
            ))

        return readings

    def run_navigation_step(self) -> bool:
        """Run one step of navigation."""
        print(f"\n--- Navigation Step {self.demo_step + 1} ---")

        # Generate simulated sensor data
        sensor_data = self.generate_simulated_sensors()
        self.navigator.update_sensors(sensor_data)

        # Display sensor information
        obstacle_count = len([s for s in sensor_data if s.distance < 1.0])
        print(f"Detected {obstacle_count} obstacles within 1m")

        # Update navigation
        nav_state = self.navigator.update_navigation()

        # Display navigation status
        status = self.navigator.get_navigation_status()
        print(f"Position: ({status['current_position'][0]:.2f}, {status['current_position'][1]:.2f})")
        print(f"Target: ({status['target_position'][0]:.2f}, {status['target_position'][1]:.2f})")
        print(f"Distance to target: {status['distance_to_target']:.2f}m")
        print(f"State: {status['navigation_state']}")
        print(f"Velocity: ({status['current_velocity'][0]:.2f}, {status['current_velocity'][1]:.2f})")

        # Check if navigation is complete
        if nav_state == NavigationState.TARGET_REACHED:
            print("SUCCESS: Target reached!")
            self.navigation_successful = True
            return False

        self.demo_step += 1
        return self.demo_step < self.max_steps and nav_state != NavigationState.STUCK

    def run_demo(self):
        """Run the complete rule-based navigation demonstration."""
        print("Rule-Based Navigation Simulation Demo")
        print("=" * 35)
        print("Simulating how a robot navigates using rule-based decision making.")
        print("The robot uses predefined rules to react to its environment and")
        print("reach its target destination.\n")

        print("Navigation rules implemented:")
        print("- Safety checks (highest priority)")
        print("- Obstacle avoidance")
        print("- Wall following")
        print("- Path correction")
        print("- Goal seeking (lowest priority)\n")

        print(f"Target: {self.navigator.current_state.target}")
        print(f"Starting position: {self.navigator.current_state.position}\n")

        # Run the navigation simulation
        while self.run_navigation_step():
            time.sleep(0.3)  # Simulate time between navigation steps

        print(f"\nDemo completed after {self.demo_step} steps")

        # Final status
        final_status = self.navigator.get_navigation_status()
        print(f"\nFinal Status:")
        print(f"  Position: {final_status['current_position']}")
        print(f"  Distance to target: {final_status['distance_to_target']:.2f}m")
        print(f"  Final state: {final_status['navigation_state']}")

        if self.navigation_successful:
            print("  Result: Navigation successful!")
        else:
            print("  Result: Navigation incomplete (hit max steps or got stuck)")


def main():
    """Main function to run the rule-based navigation simulation."""
    demo = RuleBasedNavigationDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()