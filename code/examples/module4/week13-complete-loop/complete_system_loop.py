"""
Complete System Loop Example

This script demonstrates a complete physical AI system loop that integrates
all the concepts learned throughout the course: sensing, perception, decision-making,
and action. It simulates a robot performing a complete task cycle.
"""

import time
import random
import math
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum


class SensorType(Enum):
    """Types of sensors in the complete system."""
    PROXIMITY = "proximity"
    CAMERA = "camera"
    GYRO = "gyro"
    ACCELEROMETER = "accelerometer"
    TEMPERATURE = "temperature"
    BATTERY = "battery"
    GPS = "gps"
    COMPASS = "compass"


class SystemState(Enum):
    """States of the complete system."""
    IDLE = "idle"
    SENSING = "sensing"
    PERCEIVING = "perceiving"
    DECIDING = "deciding"
    ACTING = "acting"
    NAVIGATING = "navigating"
    INTERACTING = "interacting"
    CHARGING = "charging"
    EMERGENCY = "emergency"


class RobotAction(Enum):
    """Actions the robot can perform."""
    MOVE_FORWARD = "move_forward"
    TURN_LEFT = "turn_left"
    TURN_RIGHT = "turn_right"
    STOP = "stop"
    BACK_UP = "back_up"
    APPROACH_OBJECT = "approach_object"
    AVOID_OBSTACLE = "avoid_obstacle"
    GRASP_OBJECT = "grasp_object"
    RELEASE_OBJECT = "release_object"
    CALL_FOR_HELP = "call_for_help"
    RETURN_HOME = "return_home"
    CHARGE_BATTERY = "charge_battery"


@dataclass
class SensorReading:
    """Represents a sensor reading."""
    sensor_type: SensorType
    value: Any
    timestamp: float
    confidence: float = 1.0


@dataclass
class EnvironmentalObject:
    """Represents an object detected in the environment."""
    id: str
    position: Tuple[float, float, float]  # x, y, z
    object_type: str  # "obstacle", "target", "charger", etc.
    importance: float  # 0.0 to 1.0
    confidence: float = 1.0


@dataclass
class RobotState:
    """Represents the complete state of the robot."""
    position: Tuple[float, float, float]  # x, y, z
    orientation: Tuple[float, float, float]  # roll, pitch, yaw
    battery_level: float  # 0.0 to 1.0
    velocity: Tuple[float, float, float]  # x, y, z velocity
    current_task: str
    carrying_object: bool = False
    system_state: SystemState = SystemState.IDLE
    sensor_readings: List[SensorReading] = None
    detected_objects: List[EnvironmentalObject] = None

    def __post_init__(self):
        if self.sensor_readings is None:
            self.sensor_readings = []
        if self.detected_objects is None:
            self.detected_objects = []


class SensingModule:
    """Handles all sensor data collection and preprocessing."""

    def __init__(self):
        self.sensors = [sensor_type for sensor_type in SensorType]
        self.last_readings: Dict[SensorType, SensorReading] = {}

    def collect_sensory_data(self) -> List[SensorReading]:
        """Simulate collecting data from all sensors."""
        readings = []
        current_time = time.time()

        # Proximity sensor (distance to nearest obstacle)
        proximity_value = random.uniform(0.1, 3.0)
        proximity_reading = SensorReading(
            sensor_type=SensorType.PROXIMITY,
            value=proximity_value,
            timestamp=current_time,
            confidence=0.9
        )
        readings.append(proximity_reading)

        # Camera sensor (object detection: (detected, importance))
        camera_detected = random.random() > 0.6
        camera_importance = random.uniform(0.0, 1.0) if camera_detected else 0.0
        camera_reading = SensorReading(
            sensor_type=SensorType.CAMERA,
            value=(camera_detected, camera_importance),
            timestamp=current_time,
            confidence=0.85
        )
        readings.append(camera_reading)

        # Gyro sensor (orientation stability)
        gyro_value = random.uniform(-0.3, 0.3)
        gyro_reading = SensorReading(
            sensor_type=SensorType.GYRO,
            value=gyro_value,
            timestamp=current_time,
            confidence=0.95
        )
        readings.append(gyro_reading)

        # Accelerometer sensor (motion detection)
        accel_x = random.uniform(-1.0, 1.0)
        accel_y = random.uniform(-1.0, 1.0)
        accel_z = random.uniform(-10.0, -8.0)  # Near gravity
        accel_reading = SensorReading(
            sensor_type=SensorType.ACCELEROMETER,
            value=(accel_x, accel_y, accel_z),
            timestamp=current_time,
            confidence=0.9
        )
        readings.append(accel_reading)

        # Temperature sensor
        temp_reading = SensorReading(
            sensor_type=SensorType.TEMPERATURE,
            value=random.uniform(20.0, 30.0),
            timestamp=current_time,
            confidence=0.8
        )
        readings.append(temp_reading)

        # Battery sensor
        battery_reading = SensorReading(
            sensor_type=SensorType.BATTERY,
            value=random.uniform(0.2, 1.0),
            timestamp=current_time,
            confidence=1.0
        )
        readings.append(battery_reading)

        # GPS sensor (position)
        gps_x = random.uniform(-10.0, 10.0)
        gps_y = random.uniform(-10.0, 10.0)
        gps_z = random.uniform(0.0, 2.0)
        gps_reading = SensorReading(
            sensor_type=SensorType.GPS,
            value=(gps_x, gps_y, gps_z),
            timestamp=current_time,
            confidence=0.95
        )
        readings.append(gps_reading)

        # Compass sensor (heading)
        compass_reading = SensorReading(
            sensor_type=SensorType.COMPASS,
            value=random.uniform(0, 2 * math.pi),
            timestamp=current_time,
            confidence=0.9
        )
        readings.append(compass_reading)

        # Update last readings
        for reading in readings:
            self.last_readings[reading.sensor_type] = reading

        return readings


class PerceptionModule:
    """Processes sensor data to understand the environment."""

    def __init__(self):
        self.known_objects: List[EnvironmentalObject] = []
        self.map = {}  # Simplified map representation

    def process_sensory_data(self, sensor_readings: List[SensorReading]) -> List[EnvironmentalObject]:
        """Process sensor data to detect and understand objects in the environment."""
        detected_objects = []

        # Process camera data to detect objects
        camera_readings = [r for r in sensor_readings if r.sensor_type == SensorType.CAMERA]
        if camera_readings:
            camera_data = camera_readings[0].value
            if isinstance(camera_data, tuple) and camera_data[0]:  # Object detected
                obj_id = f"obj_{len(self.known_objects) + 1}"
                importance = camera_data[1] if len(camera_data) > 1 else 0.5

                # Estimate position based on other sensors
                proximity_readings = [r for r in sensor_readings if r.sensor_type == SensorType.PROXIMITY]
                gps_readings = [r for r in sensor_readings if r.sensor_type == SensorType.GPS]

                x, y, z = 0, 0, 0
                if gps_readings:
                    gps_pos = gps_readings[0].value
                    x, y, z = gps_pos[0], gps_pos[1], gps_pos[2]

                # Adjust position based on proximity to make it more realistic
                if proximity_readings:
                    proximity_dist = proximity_readings[0].value
                    compass_readings = [r for r in sensor_readings if r.sensor_type == SensorType.COMPASS]
                    if compass_readings:
                        heading = compass_readings[0].value
                        x += proximity_dist * math.cos(heading)
                        y += proximity_dist * math.sin(heading)

                obj_type = "target" if importance > 0.7 else "obstacle" if importance > 0.3 else "background"
                obj = EnvironmentalObject(
                    id=obj_id,
                    position=(x, y, z),
                    object_type=obj_type,
                    importance=importance,
                    confidence=camera_readings[0].confidence
                )
                detected_objects.append(obj)
                self.known_objects.append(obj)

        # Process proximity data for obstacles
        proximity_readings = [r for r in sensor_readings if r.sensor_type == SensorType.PROXIMITY]
        if proximity_readings and proximity_readings[0].value < 0.5:
            # Close obstacle detected
            obj_id = f"obs_{len(self.known_objects) + 1}"
            gps_readings = [r for r in sensor_readings if r.sensor_type == SensorType.GPS]
            compass_readings = [r for r in sensor_readings if r.sensor_type == SensorType.COMPASS]

            x, y, z = 0, 0, 0
            if gps_readings:
                gps_pos = gps_readings[0].value
                x, y, z = gps_pos[0], gps_pos[1], gps_pos[2]

            if compass_readings:
                heading = compass_readings[0].value
                proximity_dist = proximity_readings[0].value
                x += proximity_dist * math.cos(heading)
                y += proximity_dist * math.sin(heading)

            obstacle = EnvironmentalObject(
                id=obj_id,
                position=(x, y, z),
                object_type="obstacle",
                importance=0.9,  # High importance for obstacles
                confidence=proximity_readings[0].confidence
            )
            detected_objects.append(obstacle)
            self.known_objects.append(obstacle)

        return detected_objects


class DecisionModule:
    """Makes decisions based on the perceived environment and current state."""

    def __init__(self):
        self.current_goal = "explore_environment"
        self.decision_history: List[Tuple[str, RobotAction]] = []

    def make_decision(self, robot_state: RobotState, detected_objects: List[EnvironmentalObject]) -> RobotAction:
        """Make a decision based on current state and perceived environment."""
        # Check for emergency conditions first
        battery_level = robot_state.battery_level
        if battery_level < 0.1:
            return RobotAction.RETURN_HOME

        # Check for immediate obstacles
        close_obstacles = [obj for obj in detected_objects if obj.object_type == "obstacle" and obj.importance > 0.8]
        if close_obstacles:
            return RobotAction.AVOID_OBSTACLE

        # Check for high-importance targets
        targets = [obj for obj in detected_objects if obj.object_type == "target" and obj.importance > 0.7]
        if targets and not robot_state.carrying_object:
            return RobotAction.APPROACH_OBJECT

        # Check if we're near a charging station
        chargers = [obj for obj in detected_objects if obj.object_type == "charger"]
        if chargers and battery_level < 0.3:
            return RobotAction.CHARGE_BATTERY

        # Default behavior based on state
        if robot_state.system_state == SystemState.NAVIGATING:
            return RobotAction.MOVE_FORWARD
        elif robot_state.system_state == SystemState.INTERACTING:
            return RobotAction.GRASP_OBJECT
        else:
            # Choose action based on battery level and environment
            if battery_level < 0.3:
                return RobotAction.RETURN_HOME
            else:
                return RobotAction.MOVE_FORWARD


class ActionModule:
    """Executes actions decided by the decision module."""

    def __init__(self):
        self.action_history: List[RobotAction] = []

    def execute_action(self, action: RobotAction, robot_state: RobotState) -> RobotState:
        """Execute the given action and update the robot state."""
        new_state = robot_state
        current_pos = robot_state.position
        current_orient = robot_state.orientation

        if action == RobotAction.MOVE_FORWARD:
            # Move forward based on current orientation
            heading = current_orient[2]  # yaw component
            new_x = current_pos[0] + 0.2 * math.cos(heading)
            new_y = current_pos[1] + 0.2 * math.sin(heading)
            new_pos = (new_x, new_y, current_pos[2])
            new_state.position = new_pos

        elif action == RobotAction.TURN_LEFT:
            # Turn left (decrease yaw)
            new_orient = (current_orient[0], current_orient[1], current_orient[2] - 0.3)
            new_state.orientation = new_orient

        elif action == RobotAction.TURN_RIGHT:
            # Turn right (increase yaw)
            new_orient = (current_orient[0], current_orient[1], current_orient[2] + 0.3)
            new_state.orientation = new_orient

        elif action == RobotAction.STOP:
            # Stop moving (no position change)
            pass

        elif action == RobotAction.BACK_UP:
            # Move backward
            heading = current_orient[2]  # yaw component
            new_x = current_pos[0] - 0.2 * math.cos(heading)
            new_y = current_pos[1] - 0.2 * math.sin(heading)
            new_pos = (new_x, new_y, current_pos[2])
            new_state.position = new_pos

        elif action == RobotAction.AVOID_OBSTACLE:
            # Turn away from the obstacle (simplified)
            new_orient = (current_orient[0], current_orient[1], current_orient[2] + 0.5)
            new_state.orientation = new_orient

        elif action == RobotAction.APPROACH_OBJECT:
            # Move toward the nearest interesting object
            if robot_state.detected_objects:
                nearest_obj = min(
                    (obj for obj in robot_state.detected_objects if obj.importance > 0.5),
                    key=lambda obj: math.sqrt(
                        (obj.position[0] - current_pos[0])**2 +
                        (obj.position[1] - current_pos[1])**2
                    ),
                    default=None
                )
                if nearest_obj:
                    dx = nearest_obj.position[0] - current_pos[0]
                    dy = nearest_obj.position[1] - current_pos[1]
                    distance = math.sqrt(dx**2 + dy**2)
                    if distance > 0.1:  # Only move if not already very close
                        new_x = current_pos[0] + (dx / distance) * 0.1
                        new_y = current_pos[1] + (dy / distance) * 0.1
                        new_pos = (new_x, new_y, current_pos[2])
                        new_state.position = new_pos

        elif action == RobotAction.RETURN_HOME:
            # Move toward origin (0, 0)
            dx = -current_pos[0]
            dy = -current_pos[1]
            distance = math.sqrt(dx**2 + dy**2)
            if distance > 0.1:
                new_x = current_pos[0] + (dx / distance) * 0.15
                new_y = current_pos[1] + (dy / distance) * 0.15
                new_pos = (new_x, new_y, current_pos[2])
                new_state.position = new_pos

        elif action == RobotAction.GRASP_OBJECT:
            # Simulate grasping an object
            new_state.carrying_object = True

        elif action == RobotAction.RELEASE_OBJECT:
            # Simulate releasing an object
            new_state.carrying_object = False

        # Consume some battery with each action
        new_state.battery_level = max(0.0, new_state.battery_level - 0.001)

        # Add to action history
        self.action_history.append(action)
        new_state.last_action = action

        return new_state


class CompleteSystemLoop:
    """Main class that orchestrates the complete system loop."""

    def __init__(self):
        self.sensing_module = SensingModule()
        self.perception_module = PerceptionModule()
        self.decision_module = DecisionModule()
        self.action_module = ActionModule()
        self.current_state = self._initialize_robot_state()
        self.loop_count = 0
        self.max_loops = 20

    def _initialize_robot_state(self) -> RobotState:
        """Initialize the robot's starting state."""
        return RobotState(
            position=(0.0, 0.0, 0.0),
            orientation=(0.0, 0.0, 0.0),  # roll, pitch, yaw
            battery_level=1.0,
            velocity=(0.0, 0.0, 0.0),
            current_task="environmental_exploration"
        )

    def run_single_loop(self) -> bool:
        """Run a single iteration of the complete system loop."""
        print(f"\n--- System Loop Iteration {self.loop_count + 1} ---")

        # 1. SENSING: Collect data from all sensors
        print("1. SENSING: Collecting sensor data...")
        self.current_state.system_state = SystemState.SENSING
        sensor_readings = self.sensing_module.collect_sensory_data()
        self.current_state.sensor_readings = sensor_readings

        # Display some sensor information
        battery_reading = next((r for r in sensor_readings if r.sensor_type == SensorType.BATTERY), None)
        proximity_reading = next((r for r in sensor_readings if r.sensor_type == SensorType.PROXIMITY), None)

        if battery_reading:
            print(f"   Battery level: {battery_reading.value:.2f}")
        if proximity_reading:
            print(f"   Proximity to nearest object: {proximity_reading.value:.2f}m")

        # 2. PERCEIVING: Process sensor data to understand environment
        print("2. PERCEIVING: Processing sensor data...")
        self.current_state.system_state = SystemState.PERCEIVING
        detected_objects = self.perception_module.process_sensory_data(sensor_readings)
        self.current_state.detected_objects = detected_objects

        print(f"   Detected {len(detected_objects)} objects:")
        for obj in detected_objects[:3]:  # Show first 3 objects
            print(f"     - {obj.object_type} at {obj.position[:2]} (importance: {obj.importance:.2f})")
        if len(detected_objects) > 3:
            print(f"     ... and {len(detected_objects) - 3} more")

        # 3. DECIDING: Make decisions based on perception
        print("3. DECIDING: Making decisions...")
        self.current_state.system_state = SystemState.DECIDING
        action = self.decision_module.make_decision(self.current_state, detected_objects)

        print(f"   Selected action: {action.value}")

        # 4. ACTING: Execute the decision
        print("4. ACTING: Executing action...")
        self.current_state.system_state = SystemState.ACTING
        self.current_state = self.action_module.execute_action(action, self.current_state)

        print(f"   New position: ({self.current_state.position[0]:.2f}, {self.current_state.position[1]:.2f})")
        print(f"   Battery: {self.current_state.battery_level:.2f}")
        print(f"   Carrying object: {self.current_state.carrying_object}")

        self.loop_count += 1
        return self.loop_count < self.max_loops

    def run_complete_system(self):
        """Run the complete system for multiple iterations."""
        print("Complete Physical AI System Loop Demo")
        print("=" * 38)
        print("Demonstrating the complete loop: Sense → Perceive → Decide → Act")
        print("This integrates all concepts learned throughout the course.\n")

        print("System modules:")
        print("- Sensing: Collects data from multiple sensors")
        print("- Perception: Processes sensor data to understand environment")
        print("- Decision: Makes choices based on state and perception")
        print("- Action: Executes decisions and updates robot state\n")

        print(f"Starting position: {self.current_state.position}")
        print(f"Initial battery: {self.current_state.battery_level}")
        print(f"Task: {self.current_state.current_task}\n")

        # Run the complete system loop
        while self.run_single_loop():
            time.sleep(0.5)  # Simulate real-time processing delay

        print(f"\nSystem completed {self.loop_count} iterations")

        # Final summary
        print(f"\nFinal State:")
        print(f"  Position: ({self.current_state.position[0]:.2f}, {self.current_state.position[1]:.2f})")
        print(f"  Battery: {self.current_state.battery_level:.2f}")
        print(f"  Carrying object: {self.current_state.carrying_object}")
        print(f"  Last action: {self.current_state.last_action.value if self.current_state.last_action else 'None'}")

        print(f"\nSystem Statistics:")
        print(f"  Total actions executed: {len(self.action_module.action_history)}")
        action_counts = {}
        for action in self.action_module.action_history:
            action_counts[action.value] = action_counts.get(action.value, 0) + 1

        print(f"  Action distribution:")
        for action, count in sorted(action_counts.items()):
            print(f"    {action}: {count}")


def main():
    """Main function to run the complete system loop simulation."""
    system = CompleteSystemLoop()
    system.run_complete_system()


if __name__ == "__main__":
    main()