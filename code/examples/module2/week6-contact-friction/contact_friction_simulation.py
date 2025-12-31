"""
Contact and Friction Simulation Example

This script demonstrates basic concepts of contact mechanics and friction
in physical AI systems. It simulates how objects interact when they come
into contact with surfaces and how friction affects their motion.
"""

import math
import time
import random
from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class PhysicalObject:
    """Represents a physical object with properties relevant to contact and friction."""
    name: str
    mass: float  # kg
    position: Tuple[float, float, float]  # x, y, z coordinates
    velocity: Tuple[float, float, float]  # velocity vector
    friction_coefficient: float  # coefficient of friction
    restitution: float  # bounciness (0 = no bounce, 1 = perfect bounce)


class ContactFrictionSimulator:
    """Simulates contact mechanics and friction between objects and surfaces."""

    def __init__(self):
        self.objects: List[PhysicalObject] = []
        self.gravity = 9.81  # m/s^2
        self.ground_level = 0.0
        self.simulation_steps = 0

    def add_object(self, obj: PhysicalObject):
        """Add an object to the simulation."""
        self.objects.append(obj)

    def calculate_normal_force(self, obj: PhysicalObject) -> float:
        """Calculate the normal force acting on an object."""
        return obj.mass * self.gravity

    def calculate_friction_force(self, obj: PhysicalObject, applied_force: float) -> float:
        """Calculate the friction force opposing motion."""
        normal_force = self.calculate_normal_force(obj)
        max_static_friction = obj.friction_coefficient * normal_force

        # If applied force is less than static friction, object doesn't move
        if abs(applied_force) <= max_static_friction:
            return -applied_force  # Static friction balances applied force
        else:
            # Kinetic friction when object is moving
            kinetic_friction = obj.friction_coefficient * normal_force
            return -math.copysign(kinetic_friction, obj.velocity[0])  # Opposes motion direction

    def detect_ground_collision(self, obj: PhysicalObject) -> bool:
        """Detect if an object collides with the ground."""
        return obj.position[1] <= self.ground_level and obj.velocity[1] < 0

    def handle_ground_collision(self, obj: PhysicalObject) -> bool:
        """Handle collision with the ground, considering friction."""
        if self.detect_ground_collision():
            # Calculate impact velocity
            impact_velocity = abs(obj.velocity[1])

            # Apply restitution (bounce effect)
            new_y_velocity = impact_velocity * obj.restitution

            # Apply friction to horizontal movement upon impact
            friction_effect = 0.95 - (obj.friction_coefficient * 0.1)
            new_x_velocity = obj.velocity[0] * friction_effect

            # Update object velocity
            obj.velocity = (new_x_velocity, -new_y_velocity, obj.velocity[2])

            # Place object at ground level to prevent sinking
            obj.position = (obj.position[0], self.ground_level, obj.position[2])

            return True
        return False

    def update_physics(self, obj: PhysicalObject, dt: float = 0.01):
        """Update the physics for a single object."""
        # Apply gravity
        new_vy = obj.velocity[1] - self.gravity * dt

        # Calculate net horizontal force (including friction)
        applied_force = 0.0  # In this simple example, no external forces
        friction_force = self.calculate_friction_force(obj, applied_force)

        # Update velocities
        new_vx = obj.velocity[0] + (friction_force / obj.mass) * dt
        new_vz = obj.velocity[2]  # Assuming no forces in z-direction

        # Update positions
        new_x = obj.position[0] + new_vx * dt
        new_y = max(self.ground_level, obj.position[1] + new_vy * dt)  # Prevent going below ground
        new_z = obj.position[2] + new_vz * dt

        # Handle ground collision
        if self.handle_ground_collision(obj):
            # After collision, we might want to apply additional friction effects
            pass

        # Update object state
        obj.velocity = (new_vx, new_vy, new_vz)
        obj.position = (new_x, new_y, new_z)

    def run_simulation_step(self, dt: float = 0.01):
        """Run one step of the simulation."""
        for obj in self.objects:
            self.update_physics(obj, dt)
        self.simulation_steps += 1

    def get_object_state(self, obj: PhysicalObject) -> dict:
        """Get the current state of an object."""
        return {
            'position': obj.position,
            'velocity': obj.velocity,
            'speed': math.sqrt(sum(v**2 for v in obj.velocity)),
            'contact_with_ground': self.detect_ground_collision(obj),
            'normal_force': self.calculate_normal_force(obj),
            'friction_coefficient': obj.friction_coefficient
        }


def demonstrate_contact_friction():
    """Demonstrate contact and friction concepts."""
    print("Contact and Friction Simulation Demo")
    print("=" * 40)

    simulator = ContactFrictionSimulator()

    # Create objects with different friction coefficients
    objects = [
        PhysicalObject(
            name="Rubber Ball",
            mass=0.5,
            position=(0.0, 5.0, 0.0),
            velocity=(2.0, 0.0, 0.0),
            friction_coefficient=0.8,  # High friction
            restitution=0.7
        ),
        PhysicalObject(
            name="Ice Cube",
            mass=0.2,
            position=(0.0, 5.0, 2.0),
            velocity=(3.0, 0.0, 0.0),
            friction_coefficient=0.1,  # Low friction
            restitution=0.1
        ),
        PhysicalObject(
            name="Wood Block",
            mass=1.0,
            position=(0.0, 5.0, -2.0),
            velocity=(1.5, 0.0, 0.0),
            friction_coefficient=0.4,  # Medium friction
            restitution=0.3
        )
    ]

    for obj in objects:
        simulator.add_object(obj)

    print("\nInitial Object States:")
    for obj in objects:
        state = simulator.get_object_state(obj)
        print(f"{obj.name}: Position={state['position']}, Velocity={state['velocity']}")

    print(f"\nSimulation running for 100 steps...")

    # Run simulation for a few steps
    for step in range(100):
        simulator.run_simulation_step(dt=0.02)

        if step % 20 == 0:  # Print state every 20 steps
            print(f"\nStep {step}:")
            for obj in objects:
                state = simulator.get_object_state(obj)
                contact_status = "GROUND CONTACT" if state['contact_with_ground'] else "IN AIR"
                print(f"  {obj.name}: Pos={state['position'][:2]}, "
                      f"Vel={state['velocity'][:2]}, Speed={state['speed']:.2f}, {contact_status}")

    print(f"\nFinal States:")
    for obj in objects:
        state = simulator.get_object_state(obj)
        contact_status = "GROUND CONTACT" if state['contact_with_ground'] else "IN AIR"
        print(f"{obj.name}: Pos={state['position']}, Vel={state['velocity']}, {contact_status}")
        print(f"  Normal Force: {state['normal_force']:.2f}N, "
              f"Friction Coefficient: {state['friction_coefficient']}")


def main():
    """Main function to run the contact and friction simulation."""
    demonstrate_contact_friction()


if __name__ == "__main__":
    main()