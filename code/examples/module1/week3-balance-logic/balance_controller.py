"""
Balance Logic Example

This script demonstrates basic balance control concepts that are fundamental to
physical systems in Physical AI. It simulates a simple inverted pendulum system
that must maintain balance through sensor feedback and control actions.
"""

import time
import math
import random
from dataclasses import dataclass
from typing import Tuple, List
from enum import Enum


class BalanceState(Enum):
    """Represents different balance states."""
    STABLE = "stable"
    WOBBLY = "wobbly"
    UNSTABLE = "unstable"
    FALLING = "falling"


@dataclass
class SensorReading:
    """Represents a sensor reading for balance control."""
    angle: float  # Angle in radians from vertical
    angular_velocity: float  # Rate of change of angle
    center_of_mass_x: float  # Horizontal position of center of mass
    center_of_mass_y: float  # Vertical position of center of mass
    timestamp: float


@dataclass
class ControlAction:
    """Represents a control action to maintain balance."""
    force_x: float  # Horizontal corrective force
    force_y: float  # Vertical corrective force (if applicable)
    torque: float  # Rotational corrective force
    duration: float  # Duration of action


class SimpleBalanceSystem:
    """Simulates a simple balance system (like an inverted pendulum)."""

    def __init__(self, initial_angle: float = 0.0, initial_angular_velocity: float = 0.0):
        self.angle = initial_angle  # Angle from vertical (radians)
        self.angular_velocity = initial_angular_velocity  # Rate of change of angle
        self.center_of_mass_x = math.sin(initial_angle) * 1.0  # Simplified CoM calculation
        self.center_of_mass_y = math.cos(initial_angle) * 1.0
        self.height = 1.0  # Height of the system
        self.mass = 10.0  # Mass of the system
        self.moment_of_inertia = self.mass * (self.height ** 2) / 3  # Simplified moment of inertia
        self.gravity = 9.81  # Gravity constant
        self.time_step = 0.01  # Simulation time step (10ms)

        # Control parameters
        self.kp_angle = 15.0  # Proportional gain for angle
        self.kd_angle = 3.0   # Derivative gain for angular velocity
        self.kp_position = 8.0  # Proportional gain for position
        self.max_force = 100.0  # Maximum corrective force
        self.max_torque = 50.0  # Maximum corrective torque

    def get_sensor_reading(self) -> SensorReading:
        """Get current sensor readings."""
        return SensorReading(
            angle=self.angle,
            angular_velocity=self.angular_velocity,
            center_of_mass_x=self.center_of_mass_x,
            center_of_mass_y=self.center_of_mass_y,
            timestamp=time.time()
        )

    def apply_control(self, action: ControlAction):
        """Apply control forces to the system."""
        # Limit forces to maximum values
        force_x = max(-self.max_force, min(self.max_force, action.force_x))
        torque = max(-self.max_torque, min(self.max_torque, action.torque))

        # Update angular acceleration based on torque
        angular_acceleration = torque / self.moment_of_inertia

        # Apply gravity effect (tends to make the system fall)
        gravity_torque = -self.mass * self.gravity * self.height * math.sin(self.angle) / 2
        gravity_effect = gravity_torque / self.moment_of_inertia

        # Update state using simple physics integration
        self.angular_velocity += (angular_acceleration + gravity_effect) * self.time_step
        self.angle += self.angular_velocity * self.time_step

        # Update center of mass position
        self.center_of_mass_x = math.sin(self.angle) * self.height
        self.center_of_mass_y = math.cos(self.angle) * self.height

    def get_balance_state(self) -> BalanceState:
        """Determine the current balance state."""
        angle_threshold = math.radians(15)  # 15 degrees
        angular_velocity_threshold = 1.0  # rad/s

        if abs(self.angle) > math.radians(45):
            return BalanceState.FALLING
        elif abs(self.angle) > angle_threshold or abs(self.angular_velocity) > angular_velocity_threshold:
            return BalanceState.UNSTABLE
        elif abs(self.angle) > math.radians(5) or abs(self.angular_velocity) > 0.3:
            return BalanceState.WOBBLY
        else:
            return BalanceState.STABLE

    def simulate_external_force(self):
        """Simulate random external forces that might affect balance."""
        if random.random() < 0.1:  # 10% chance per time step
            # Apply a random external torque
            external_torque = random.uniform(-5.0, 5.0)
            self.angular_velocity += external_torque / self.moment_of_inertia * self.time_step


class BalanceController:
    """Implements balance control logic."""

    def __init__(self, system: SimpleBalanceSystem):
        self.system = system
        self.control_history: List[Tuple[float, ControlAction]] = []

    def calculate_control_action(self, sensor_reading: SensorReading) -> ControlAction:
        """Calculate control action based on sensor reading."""
        # Proportional control for angle (correct toward vertical)
        angle_correction = -sensor_reading.angle * self.system.kp_angle

        # Derivative control for angular velocity (dampen oscillations)
        velocity_correction = -sensor_reading.angular_velocity * self.system.kd_angle

        # Combined corrective torque
        torque = angle_correction + velocity_correction

        # Position-based correction (simplified)
        position_correction = -sensor_reading.center_of_mass_x * self.system.kp_position
        force_x = position_correction

        # Create control action
        action = ControlAction(
            force_x=force_x,
            force_y=0.0,  # Not using vertical force in this simple model
            torque=torque,
            duration=self.system.time_step
        )

        # Store in history
        self.control_history.append((sensor_reading.timestamp, action))

        return action

    def get_performance_metrics(self) -> dict:
        """Calculate performance metrics."""
        if not self.control_history:
            return {"stability_score": 0.0, "avg_control_effort": 0.0}

        # Calculate average control effort
        total_effort = 0.0
        for _, action in self.control_history[-100:]:  # Last 100 actions
            total_effort += abs(action.torque) + abs(action.force_x)

        avg_effort = total_effort / len(self.control_history[-100:]) if self.control_history[-100:] else 0.0

        # Stability score (simplified: inverse of average angle deviation)
        recent_angles = [abs(action.torque / self.system.kp_angle) if abs(action.torque) > 0.1
                        else 0.0 for _, action in self.control_history[-50:]]
        avg_angle_deviation = sum(recent_angles) / len(recent_angles) if recent_angles else 0.0
        stability_score = max(0.0, 10.0 - avg_angle_deviation * 10)  # Higher is better

        return {
            "stability_score": min(10.0, stability_score),
            "avg_control_effort": avg_effort,
            "total_corrections": len(self.control_history)
        }


class BalanceDemo:
    """Main demonstration class for the balance system."""

    def __init__(self):
        self.system = SimpleBalanceSystem(initial_angle=math.radians(5))  # Start with small angle
        self.controller = BalanceController(self.system)
        self.demo_steps = 0
        self.max_steps = 500  # Run for 5 seconds (500 * 0.01s)

    def run_step(self) -> bool:
        """Run one step of the balance simulation."""
        # Get sensor reading
        reading = self.system.get_sensor_reading()

        # Determine current state
        state = self.system.get_balance_state()

        # Calculate control action
        action = self.controller.calculate_control_action(reading)

        # Apply control action
        self.system.apply_control(action)

        # Simulate external disturbances
        self.system.simulate_external_force()

        # Print status occasionally
        if self.demo_steps % 50 == 0:
            print(f"Step {self.demo_steps}: Angle={math.degrees(reading.angle):.2f}°, "
                  f"State={state.value}, Torque={action.torque:.2f}")

        self.demo_steps += 1

        # Check if we should continue
        return self.demo_steps < self.max_steps and state != BalanceState.FALLING

    def run_demo(self):
        """Run the complete balance demonstration."""
        print("Physical AI Balance Control Demo")
        print("=" * 40)
        print(f"Initial angle: {math.degrees(self.system.angle):.2f} degrees")
        print(f"Target: Maintain balance around 0 degrees\n")

        start_time = time.time()

        # Run the simulation
        while self.run_step():
            # Small delay to make it observable (optional in real-time)
            time.sleep(0.001)  # 1ms delay to not overwhelm the console

        elapsed_time = time.time() - start_time

        # Print final results
        final_state = self.system.get_balance_state()
        metrics = self.controller.get_performance_metrics()

        print(f"\nDemo completed after {elapsed_time:.2f} seconds")
        print(f"Final angle: {math.degrees(self.system.angle):.2f} degrees")
        print(f"Final state: {final_state.value}")
        print(f"Balance maintained: {final_state != BalanceState.FALLING}")
        print(f"\nPerformance Metrics:")
        print(f"  Stability Score: {metrics['stability_score']:.2f}/10.0")
        print(f"  Avg Control Effort: {metrics['avg_control_effort']:.2f}")
        print(f"  Total Corrections: {metrics['total_corrections']}")


def main():
    """Main function to run the balance control demonstration."""
    demo = BalanceDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()