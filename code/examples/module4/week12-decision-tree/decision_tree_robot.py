"""
Decision Tree for Robot Decision Making Example

This script demonstrates concepts of decision trees applied to robot decision-making.
It simulates how a robot can use decision trees to make choices based on sensor
input and environmental conditions.
"""

import time
import random
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Union
from enum import Enum


class SensorType(Enum):
    """Types of sensors a robot might have."""
    PROXIMITY = "proximity"
    CAMERA = "camera"
    GYRO = "gyro"
    ACCELEROMETER = "accelerometer"
    MICROPHONE = "microphone"
    TEMPERATURE = "temperature"


class RobotAction(Enum):
    """Possible actions a robot can take."""
    MOVE_FORWARD = "move_forward"
    TURN_LEFT = "turn_left"
    TURN_RIGHT = "turn_right"
    STOP = "stop"
    BACK_UP = "back_up"
    CALL_FOR_HELP = "call_for_help"
    AVOID_OBSTACLE = "avoid_obstacle"
    APPROACH_OBJECT = "approach_object"
    IGNORE_OBJECT = "ignore_object"


class DecisionNode:
    """Represents a node in the decision tree."""

    def __init__(self, feature: str, threshold: float, feature_type: str = "numeric"):
        self.feature = feature
        self.threshold = threshold
        self.feature_type = feature_type
        self.left: Optional['DecisionNode'] = None  # For values <= threshold
        self.right: Optional['DecisionNode'] = None  # For values > threshold
        self.prediction: Optional[RobotAction] = None  # If this is a leaf node

    def is_leaf(self) -> bool:
        """Check if this is a leaf node."""
        return self.prediction is not None


@dataclass
class SensorReading:
    """Represents a sensor reading."""
    sensor_type: SensorType
    value: Union[float, str, bool]
    timestamp: float
    confidence: float = 1.0


@dataclass
class RobotState:
    """Represents the current state of the robot."""
    position: tuple  # (x, y)
    heading: float  # in radians
    battery_level: float  # 0.0 to 1.0
    sensor_readings: List[SensorReading]
    last_action: Optional[RobotAction] = None
    goal_reached: bool = False


class DecisionTreeRobot:
    """Robot that makes decisions using a decision tree."""

    def __init__(self):
        self.decision_tree = self._build_default_tree()
        self.current_state: Optional[RobotState] = None
        self.decision_history: List[Tuple[Dict, RobotAction]] = []

    def _build_default_tree(self) -> DecisionNode:
        """
        Build a default decision tree for navigation and obstacle avoidance.
        This is a simple example tree structure.
        """
        # Root: Check proximity sensor
        root = DecisionNode("proximity_distance", 0.5)  # 0.5m threshold

        # Left branch (obstacle close <= 0.5m): Check battery
        battery_check = DecisionNode("battery_level", 0.3)  # 30% battery threshold
        battery_check.left = DecisionNode("battery_level", 0.3)  # Low battery actions
        battery_check.left.prediction = RobotAction.CALL_FOR_HELP
        battery_check.right = DecisionNode("gyro_angle", 0.2)  # Check stability
        battery_check.right.left = DecisionNode("gyro_angle", 0.2)
        battery_check.right.left.prediction = RobotAction.AVOID_OBSTACLE
        battery_check.right.right = DecisionNode("gyro_angle", 0.2)
        battery_check.right.right.prediction = RobotAction.TURN_LEFT

        # Right branch (no close obstacle > 0.5m): Check camera
        camera_check = DecisionNode("camera_object_detected", 0.5)  # Binary: 0 or 1
        camera_check.left = DecisionNode("camera_object_detected", 0.5)
        camera_check.left.prediction = RobotAction.MOVE_FORWARD
        camera_check.right = DecisionNode("camera_object_importance", 0.7)  # Importance score
        camera_check.right.left = DecisionNode("camera_object_importance", 0.7)
        camera_check.right.left.prediction = RobotAction.IGNORE_OBJECT
        camera_check.right.right = DecisionNode("camera_object_importance", 0.7)
        camera_check.right.right.prediction = RobotAction.APPROACH_OBJECT

        # Connect root to branches
        root.left = battery_check
        root.right = camera_check

        return root

    def make_decision(self, state: RobotState) -> RobotAction:
        """Make a decision based on the current state using the decision tree."""
        # Convert robot state to feature dictionary
        features = self._state_to_features(state)

        # Traverse the decision tree
        current_node = self.decision_tree
        while not current_node.is_leaf():
            feature_value = features.get(current_node.feature, 0.0)

            # Handle different feature types
            if current_node.feature_type == "numeric":
                if feature_value <= current_node.threshold:
                    current_node = current_node.left
                else:
                    current_node = current_node.right
            elif current_node.feature_type == "binary":
                if feature_value <= current_node.threshold:
                    current_node = current_node.left
                else:
                    current_node = current_node.right
            else:
                # Default to left for unknown types
                current_node = current_node.left

        # Record the decision
        self.decision_history.append((features, current_node.prediction))
        return current_node.prediction

    def _state_to_features(self, state: RobotState) -> Dict[str, float]:
        """Convert robot state to feature dictionary for decision tree."""
        features = {
            'battery_level': state.battery_level,
            'proximity_distance': 10.0,  # Default to far
            'camera_object_detected': 0.0,  # Default to no object
            'camera_object_importance': 0.0,  # Default to low importance
            'gyro_angle': 0.0,  # Default to stable
            'acceleration_magnitude': 0.0,  # Default to no acceleration
        }

        # Extract features from sensor readings
        for reading in state.sensor_readings:
            if reading.sensor_type == SensorType.PROXIMITY:
                features['proximity_distance'] = float(reading.value)
            elif reading.sensor_type == SensorType.CAMERA:
                # Assume camera value is a tuple (detected, importance) or just a boolean
                if isinstance(reading.value, tuple):
                    features['camera_object_detected'] = 1.0 if reading.value[0] else 0.0
                    features['camera_object_importance'] = float(reading.value[1]) if len(reading.value) > 1 else 0.0
                else:
                    features['camera_object_detected'] = 1.0 if reading.value else 0.0
            elif reading.sensor_type == SensorType.GYRO:
                features['gyro_angle'] = abs(float(reading.value))
            elif reading.sensor_type == SensorType.ACCELEROMETER:
                if isinstance(reading.value, tuple) and len(reading.value) >= 3:
                    # Calculate magnitude of acceleration
                    ax, ay, az = reading.value
                    features['acceleration_magnitude'] = (ax**2 + ay**2 + az**2)**0.5
                else:
                    features['acceleration_magnitude'] = abs(float(reading.value))

        return features

    def update_state(self, new_state: RobotState):
        """Update the robot's state."""
        self.current_state = new_state

    def get_decision_tree_stats(self) -> Dict[str, Any]:
        """Get statistics about the decision tree."""
        def count_nodes(node: DecisionNode) -> tuple:
            """Count total nodes and leaf nodes."""
            if node.is_leaf():
                return 1, 1  # (total, leaves)
            left_total, left_leaves = count_nodes(node.left) if node.left else (0, 0)
            right_total, right_leaves = count_nodes(node.right) if node.right else (0, 0)
            return 1 + left_total + right_total, left_leaves + right_leaves

        total_nodes, leaf_nodes = count_nodes(self.decision_tree)
        return {
            'total_nodes': total_nodes,
            'leaf_nodes': leaf_nodes,
            'internal_nodes': total_nodes - leaf_nodes,
            'decision_depth': self._get_max_depth(self.decision_tree)
        }

    def _get_max_depth(self, node: DecisionNode) -> int:
        """Get the maximum depth of the tree."""
        if node.is_leaf():
            return 1
        left_depth = self._get_max_depth(node.left) if node.left else 0
        right_depth = self._get_max_depth(node.right) if node.right else 0
        return 1 + max(left_depth, right_depth)


class DecisionTreeDemo:
    """Main demonstration class for decision tree robot."""

    def __init__(self):
        self.robot = DecisionTreeRobot()
        self.demo_step = 0
        self.max_steps = 15

    def generate_simulated_sensor_readings(self) -> List[SensorReading]:
        """Generate simulated sensor readings."""
        readings = []

        # Proximity sensor (distance to nearest obstacle)
        proximity_distance = random.uniform(0.1, 2.0)
        readings.append(SensorReading(
            sensor_type=SensorType.PROXIMITY,
            value=proximity_distance,
            timestamp=time.time(),
            confidence=0.9
        ))

        # Camera sensor (object detection: (detected, importance))
        object_detected = random.random() > 0.7
        object_importance = random.uniform(0.0, 1.0) if object_detected else 0.0
        readings.append(SensorReading(
            sensor_type=SensorType.CAMERA,
            value=(object_detected, object_importance),
            timestamp=time.time(),
            confidence=0.85
        ))

        # Gyro sensor (stability reading)
        gyro_reading = random.uniform(-0.5, 0.5)
        readings.append(SensorReading(
            sensor_type=SensorType.GYRO,
            value=gyro_reading,
            timestamp=time.time(),
            confidence=0.95
        ))

        # Accelerometer sensor (acceleration vector)
        accel_x = random.uniform(-2.0, 2.0)
        accel_y = random.uniform(-2.0, 2.0)
        accel_z = random.uniform(-10.0, -8.0)  # Near gravity
        readings.append(SensorReading(
            sensor_type=SensorType.ACCELEROMETER,
            value=(accel_x, accel_y, accel_z),
            timestamp=time.time(),
            confidence=0.9
        ))

        return readings

    def run_decision_step(self) -> bool:
        """Run one step of decision making."""
        print(f"\n--- Decision Step {self.demo_step + 1} ---")

        # Generate simulated state
        battery_level = random.uniform(0.2, 1.0)
        position = (random.uniform(-10, 10), random.uniform(-10, 10))
        heading = random.uniform(0, 2 * math.pi)

        sensor_readings = self.generate_simulated_sensor_readings()

        state = RobotState(
            position=position,
            heading=heading,
            battery_level=battery_level,
            sensor_readings=sensor_readings
        )

        # Make a decision
        action = self.robot.make_decision(state)
        print(f"Robot state:")
        print(f"  Position: ({position[0]:.2f}, {position[1]:.2f})")
        print(f"  Battery: {battery_level:.2f}")
        print(f"  Proximity: {next((r.value for r in sensor_readings if r.sensor_type == SensorType.PROXIMITY), 'N/A')}m")

        print(f"Decision: {action.value}")

        # Show the feature values that led to this decision
        features = self.robot._state_to_features(state)
        print(f"Features: {features}")

        self.demo_step += 1
        return self.demo_step < self.max_steps

    def run_demo(self):
        """Run the complete decision tree demonstration."""
        print("Decision Tree Robot Simulation Demo")
        print("=" * 35)
        print("Simulating how a robot uses a decision tree to make choices based on")
        print("sensor input and environmental conditions.\n")

        print("Decision tree structure:")
        print("- Root: Check proximity sensor for obstacles")
        print("- If obstacle close: Check battery level and stability")
        print("- If no close obstacle: Check camera for objects")
        print("- Each branch leads to appropriate robot action\n")

        # Show initial tree stats
        tree_stats = self.robot.get_decision_tree_stats()
        print(f"Initial Decision Tree Stats:")
        print(f"  Total nodes: {tree_stats['total_nodes']}")
        print(f"  Leaf nodes: {tree_stats['leaf_nodes']}")
        print(f"  Max depth: {tree_stats['decision_depth']}\n")

        # Run the decision simulation
        while self.run_decision_step():
            time.sleep(0.4)  # Simulate processing time

        print(f"\nDemo completed after {self.demo_step} decision steps")

        # Final summary
        final_stats = self.robot.get_decision_tree_stats()
        print(f"\nFinal Decision Tree Stats:")
        for key, value in final_stats.items():
            print(f"  {key}: {value}")

        print(f"\nTotal decisions made: {len(self.robot.decision_history)}")
        action_counts = {}
        for _, action in self.robot.decision_history:
            action_counts[action.value] = action_counts.get(action.value, 0) + 1

        print(f"Action distribution:")
        for action, count in action_counts.items():
            print(f"  {action}: {count}")


def main():
    """Main function to run the decision tree simulation."""
    demo = DecisionTreeDemo()
    demo.run_demo()


if __name__ == "__main__":
    import math  # Need math for the demo
    main()