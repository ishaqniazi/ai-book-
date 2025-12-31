"""
Embodiment Concepts Simulation

This script demonstrates the core concepts of Physical AI embodiment:
- Digital Brain: Processing and decision-making component
- Physical Body: Sensing and action capabilities
- The loop of sensing, thinking, and acting
"""

import time
import random
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SensorReading:
    """Represents a sensor reading from the environment."""
    sensor_type: str
    value: float
    timestamp: float
    location: tuple = (0, 0)


@dataclass
class EnvironmentState:
    """Represents the state of the environment."""
    objects: List[dict]  # List of objects in environment
    obstacles: List[tuple]  # List of obstacle coordinates
    light_level: float  # Light level (0.0 to 1.0)
    temperature: float  # Temperature in Celsius


@dataclass
class Action:
    """Represents an action that can be taken by the physical body."""
    action_type: str  # 'move', 'grasp', 'rotate', etc.
    parameters: dict
    priority: int = 1


class SimpleEnvironment:
    """A simple simulated environment for the embodiment demonstration."""

    def __init__(self):
        self.state = EnvironmentState(
            objects=[
                {"type": "ball", "position": (2, 3), "color": "red"},
                {"type": "box", "position": (5, 1), "size": "small"},
                {"type": "light", "position": (0, 4), "intensity": 0.8}
            ],
            obstacles=[(3, 2), (4, 2)],
            light_level=0.6,
            temperature=22.0
        )

    def get_sensor_data(self, position: tuple) -> List[SensorReading]:
        """Simulate sensor readings at a given position."""
        readings = []

        # Simulate proximity sensor
        for obj in self.state.objects:
            dist = ((obj["position"][0] - position[0])**2 +
                   (obj["position"][1] - position[1])**2)**0.5
            if dist < 3:  # Within sensor range
                readings.append(SensorReading(
                    sensor_type="proximity",
                    value=dist,
                    timestamp=time.time(),
                    location=obj["position"]
                ))

        # Simulate light sensor
        readings.append(SensorReading(
            sensor_type="light",
            value=self.state.light_level,
            timestamp=time.time(),
            location=position
        ))

        # Simulate temperature sensor
        readings.append(SensorReading(
            sensor_type="temperature",
            value=self.state.temperature,
            timestamp=time.time(),
            location=position
        ))

        return readings

    def execute_action(self, action: Action, current_pos: tuple) -> tuple:
        """Execute an action and return new position."""
        if action.action_type == "move":
            direction = action.parameters.get("direction", "forward")
            distance = action.parameters.get("distance", 1)

            if direction == "forward":
                new_pos = (current_pos[0], current_pos[1] + distance)
            elif direction == "backward":
                new_pos = (current_pos[0], current_pos[1] - distance)
            elif direction == "left":
                new_pos = (current_pos[0] - distance, current_pos[1])
            elif direction == "right":
                new_pos = (current_pos[0] + distance, current_pos[1])
            else:
                new_pos = current_pos

            # Check for obstacles
            if new_pos in self.state.obstacles:
                print(f"Obstacle detected at {new_pos}, cannot move there")
                return current_pos

            return new_pos

        return current_pos


class DigitalBrain:
    """Represents the digital intelligence component."""

    def __init__(self):
        self.memory = []  # Store past experiences
        self.goals = ["explore_environment", "avoid_obstacles"]

    def process_sensory_input(self, readings: List[SensorReading]) -> List[Action]:
        """Process sensor readings and generate actions."""
        actions = []

        # Analyze proximity readings
        close_objects = [r for r in readings if r.sensor_type == "proximity" and r.value < 1.5]

        if close_objects:
            # If something is close, consider avoiding or investigating
            closest = min(close_objects, key=lambda x: x.value)
            if closest.value < 0.5:  # Very close - avoid
                actions.append(Action(
                    action_type="move",
                    parameters={"direction": "backward", "distance": 1},
                    priority=2
                ))
            else:  # Investigate
                actions.append(Action(
                    action_type="move",
                    parameters={"direction": "forward", "distance": 0.5},
                    priority=1
                ))
        else:
            # If nothing close, explore randomly
            directions = ["forward", "left", "right"]
            chosen_dir = random.choice(directions)
            actions.append(Action(
                action_type="move",
                parameters={"direction": chosen_dir, "distance": 1},
                priority=1
            ))

        return actions


class PhysicalBody:
    """Represents the physical component that can sense and act."""

    def __init__(self, initial_position: tuple = (0, 0)):
        self.position = initial_position
        self.sensors_active = True
        self.actuators_active = True

    def sense(self, environment: SimpleEnvironment) -> List[SensorReading]:
        """Gather sensory information from the environment."""
        if not self.sensors_active:
            return []

        return environment.get_sensor_data(self.position)

    def act(self, action: Action, environment: SimpleEnvironment) -> tuple:
        """Execute an action in the environment."""
        if not self.actuators_active:
            return self.position

        new_position = environment.execute_action(action, self.position)
        self.position = new_position
        return new_position


class EmbodiedAISystem:
    """The complete embodied AI system combining digital brain and physical body."""

    def __init__(self):
        self.digital_brain = DigitalBrain()
        self.physical_body = PhysicalBody()
        self.environment = SimpleEnvironment()
        self.time_step = 0.5  # seconds between cycles

    def run_cycle(self) -> bool:
        """Run one complete sensing-thinking-acting cycle."""
        print(f"\n--- Cycle at position {self.physical_body.position} ---")

        # 1. Sense the environment
        print("Sensing environment...")
        sensor_readings = self.physical_body.sense(self.environment)

        for reading in sensor_readings:
            print(f"  {reading.sensor_type}: {reading.value} at {reading.location}")

        # 2. Process and think (Digital Brain)
        print("Processing sensory input...")
        actions = self.digital_brain.process_sensory_input(sensor_readings)

        if actions:
            # Execute highest priority action
            action = max(actions, key=lambda a: a.priority)
            print(f"Decided to {action.action_type} with {action.parameters}")

            # 3. Act in the environment
            print("Executing action...")
            new_position = self.physical_body.act(action, self.environment)

            if new_position != self.physical_body.position:
                print(f"Moved to new position: {new_position}")
                self.physical_body.position = new_position
            else:
                print("Action had no effect or was blocked")
        else:
            print("No actions decided")

        # Small delay to simulate real-time processing
        time.sleep(self.time_step)

        return True  # Continue running


def main():
    """Main function to demonstrate the embodiment concepts."""
    print("Physical AI Embodiment Concepts Demonstration")
    print("=" * 50)

    # Create the embodied system
    system = EmbodiedAISystem()

    print("Initial position:", system.physical_body.position)
    print("Starting the sensing-thinking-acting cycle...\n")

    # Run for a number of cycles
    for cycle in range(10):
        print(f"Cycle {cycle + 1}/10")
        continue_running = system.run_cycle()

        if not continue_running:
            break

    print("\nDemonstration completed!")
    print(f"Final position: {system.physical_body.position}")

    # Summarize the journey
    print("\nSummary:")
    print("- Demonstrated the sensing-thinking-acting loop")
    print("- Showed how digital intelligence connects to physical action")
    print("- Illustrated environment interaction and adaptation")


if __name__ == "__main__":
    main()