"""
Rule-Based Robot Decision Making Example

This script demonstrates concepts of rule-based systems for robot decision-making.
It simulates how a robot can make decisions based on predefined rules and conditions
derived from sensor data and environmental context.
"""

import time
import random
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum


class SensorType(Enum):
    """Types of sensors a robot might have."""
    PROXIMITY = "proximity"
    CAMERA = "camera"
    GYRO = "gyro"
    ACCELEROMETER = "accelerometer"
    MICROPHONE = "microphone"
    TEMPERATURE = "temperature"
    BATTERY = "battery"


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
    RETURN_HOME = "return_home"
    CHARGE_BATTERY = "charge_battery"


class RuleCondition:
    """Represents a condition in a rule."""

    def __init__(self, sensor_type: SensorType, operator: str, threshold: float):
        self.sensor_type = sensor_type
        self.operator = operator  # '>', '<', '>=', '<=', '==', '!='
        self.threshold = threshold

    def evaluate(self, sensor_value: float) -> bool:
        """Evaluate the condition against a sensor value."""
        if self.operator == '>':
            return sensor_value > self.threshold
        elif self.operator == '<':
            return sensor_value < self.threshold
        elif self.operator == '>=':
            return sensor_value >= self.threshold
        elif self.operator == '<=':
            return sensor_value <= self.threshold
        elif self.operator == '==':
            return sensor_value == self.threshold
        elif self.operator == '!=':
            return sensor_value != self.threshold
        else:
            return False


class Rule:
    """Represents a rule with conditions and an action."""

    def __init__(self, name: str, conditions: List[RuleCondition], action: RobotAction, priority: int = 1):
        self.name = name
        self.conditions = conditions
        self.action = action
        self.priority = priority  # Higher number means higher priority

    def evaluate(self, sensor_values: Dict[SensorType, float]) -> bool:
        """Evaluate all conditions in the rule."""
        for condition in self.conditions:
            sensor_value = sensor_values.get(condition.sensor_type, 0.0)
            if not condition.evaluate(sensor_value):
                return False
        return True


@dataclass
class SensorReading:
    """Represents a sensor reading."""
    sensor_type: SensorType
    value: float
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


class RuleBasedRobot:
    """Robot that makes decisions using rule-based systems."""

    def __init__(self):
        self.rules = self._initialize_rules()
        self.current_state: Optional[RobotState] = None
        self.decision_history: List[Tuple[Dict, RobotAction]] = []

    def _initialize_rules(self) -> List[Rule]:
        """Initialize the rule base for the robot."""
        return [
            # High priority: Safety rules
            Rule(
                name="Emergency Stop",
                conditions=[RuleCondition(SensorType.PROXIMITY, '<', 0.2)],
                action=RobotAction.STOP,
                priority=10
            ),
            Rule(
                name="Critical Battery",
                conditions=[RuleCondition(SensorType.BATTERY, '<', 0.1)],
                action=RobotAction.RETURN_HOME,
                priority=9
            ),
            Rule(
                name="Low Battery",
                conditions=[RuleCondition(SensorType.BATTERY, '<', 0.2)],
                action=RobotAction.RETURN_HOME,
                priority=8
            ),
            # Medium priority: Obstacle avoidance
            Rule(
                name="Avoid Close Obstacle",
                conditions=[RuleCondition(SensorType.PROXIMITY, '<', 0.5)],
                action=RobotAction.AVOID_OBSTACLE,
                priority=7
            ),
            Rule(
                name="Turn Left for Obstacle",
                conditions=[
                    RuleCondition(SensorType.PROXIMITY, '<', 0.7),
                    RuleCondition(SensorType.GYRO, '>', 0.3)
                ],
                action=RobotAction.TURN_LEFT,
                priority=6
            ),
            # Lower priority: Navigation and interaction
            Rule(
                name="Approach Important Object",
                conditions=[
                    RuleCondition(SensorType.CAMERA, '>', 0.8),
                    RuleCondition(SensorType.PROXIMITY, '>', 1.0)
                ],
                action=RobotAction.APPROACH_OBJECT,
                priority=5
            ),
            Rule(
                name="Ignore Unimportant Object",
                conditions=[
                    RuleCondition(SensorType.CAMERA, '<', 0.3),
                    RuleCondition(SensorType.PROXIMITY, '>', 1.0)
                ],
                action=RobotAction.IGNORE_OBJECT,
                priority=4
            ),
            Rule(
                name="Move Forward by Default",
                conditions=[RuleCondition(SensorType.PROXIMITY, '>', 1.0)],
                action=RobotAction.MOVE_FORWARD,
                priority=1
            )
        ]

    def make_decision(self, state: RobotState) -> RobotAction:
        """Make a decision based on rules and current state."""
        # Convert sensor readings to a dictionary
        sensor_values = {}
        for reading in state.sensor_readings:
            sensor_values[reading.sensor_type] = float(reading.value)

        # Add battery level as a sensor value
        sensor_values[SensorType.BATTERY] = state.battery_level

        # Evaluate all rules and collect those that match
        applicable_rules = []
        for rule in self.rules:
            if rule.evaluate(sensor_values):
                applicable_rules.append(rule)

        # If no rules match, return a default action
        if not applicable_rules:
            return RobotAction.MOVE_FORWARD

        # Select the rule with the highest priority
        selected_rule = max(applicable_rules, key=lambda r: r.priority)

        # Record the decision
        self.decision_history.append((sensor_values, selected_rule.action))
        return selected_rule.action

    def add_rule(self, rule: Rule):
        """Add a new rule to the rule base."""
        self.rules.append(rule)
        # Sort rules by priority (highest first)
        self.rules.sort(key=lambda r: r.priority, reverse=True)

    def get_active_rules(self, state: RobotState) -> List[Rule]:
        """Get all rules that are active in the current state."""
        sensor_values = {}
        for reading in state.sensor_readings:
            sensor_values[reading.sensor_type] = float(reading.value)
        sensor_values[SensorType.BATTERY] = state.battery_level

        active_rules = []
        for rule in self.rules:
            if rule.evaluate(sensor_values):
                active_rules.append(rule)
        return active_rules

    def get_rule_stats(self) -> Dict[str, Any]:
        """Get statistics about the rule base."""
        return {
            'total_rules': len(self.rules),
            'priority_levels': list(set(rule.priority for rule in self.rules)),
            'highest_priority': max(rule.priority for rule in self.rules) if self.rules else 0,
            'lowest_priority': min(rule.priority for rule in self.rules) if self.rules else 0
        }


class RuleBasedDemo:
    """Main demonstration class for rule-based robot."""

    def __init__(self):
        self.robot = RuleBasedRobot()
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

        # Camera sensor (object importance score: 0.0 to 1.0)
        object_importance = random.uniform(0.0, 1.0)
        readings.append(SensorReading(
            sensor_type=SensorType.CAMERA,
            value=object_importance,
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

        # Accelerometer sensor (magnitude of acceleration)
        accel_magnitude = random.uniform(0.0, 2.0)
        readings.append(SensorReading(
            sensor_type=SensorType.ACCELEROMETER,
            value=accel_magnitude,
            timestamp=time.time(),
            confidence=0.9
        ))

        return readings

    def run_decision_step(self) -> bool:
        """Run one step of rule-based decision making."""
        print(f"\n--- Rule-Based Decision Step {self.demo_step + 1} ---")

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

        # Make a decision based on rules
        action = self.robot.make_decision(state)

        # Show sensor values
        print(f"Sensor readings:")
        for reading in sensor_readings:
            print(f"  {reading.sensor_type.value}: {reading.value:.2f}")

        print(f"Battery level: {battery_level:.2f}")

        # Show which rules were active
        active_rules = self.robot.get_active_rules(state)
        if active_rules:
            print(f"Active rules: {[rule.name for rule in active_rules[:3]]}")  # Show first 3
            if len(active_rules) > 3:
                print(f"  ... and {len(active_rules) - 3} more")
        else:
            print("Active rules: None")

        print(f"Selected action: {action.value}")

        self.demo_step += 1
        return self.demo_step < self.max_steps

    def run_demo(self):
        """Run the complete rule-based decision making demonstration."""
        print("Rule-Based Robot Decision Making Simulation Demo")
        print("=" * 48)
        print("Simulating how a robot makes decisions using a rule-based system.")
        print("The robot evaluates conditions from sensor data against predefined rules")
        print("and selects actions based on rule priorities.\n")

        print("Rule categories demonstrated:")
        print("- Safety rules (highest priority)")
        print("- Battery management rules")
        print("- Obstacle avoidance rules")
        print("- Navigation and interaction rules\n")

        # Show initial rule stats
        rule_stats = self.robot.get_rule_stats()
        print(f"Initial Rule Base Stats:")
        print(f"  Total rules: {rule_stats['total_rules']}")
        print(f"  Priority range: {rule_stats['lowest_priority']} to {rule_stats['highest_priority']}\n")

        # Run the decision simulation
        while self.run_decision_step():
            time.sleep(0.4)  # Simulate processing time

        print(f"\nDemo completed after {self.demo_step} decision steps")

        # Final summary
        final_stats = self.robot.get_rule_stats()
        print(f"\nFinal Rule Base Stats:")
        for key, value in final_stats.items():
            print(f"  {key}: {value}")

        print(f"\nTotal decisions made: {len(self.robot.decision_history)}")
        action_counts = {}
        for _, action in self.robot.decision_history:
            action_counts[action.value] = action_counts.get(action.value, 0) + 1

        print(f"Action distribution:")
        for action, count in sorted(action_counts.items()):
            print(f"  {action}: {count}")


def main():
    """Main function to run the rule-based robot simulation."""
    demo = RuleBasedDemo()
    demo.run_demo()


if __name__ == "__main__":
    import math  # Need math for the demo
    main()