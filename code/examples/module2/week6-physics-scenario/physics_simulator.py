"""
Physics Scenario Example

This script demonstrates basic physics simulation concepts relevant to Physical AI systems.
It simulates simple physical interactions and demonstrates how physics principles apply
to robot-environment interaction.
"""

import math
import time
from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum


class ObjectType(Enum):
    """Types of objects in the simulation."""
    SPHERE = "sphere"
    CUBE = "cube"
    PLANE = "plane"
    ROBOT = "robot"


@dataclass
class Vector3D:
    """Represents a 3D vector for position, velocity, and force calculations."""
    x: float
    y: float
    z: float

    def magnitude(self) -> float:
        """Calculate the magnitude of the vector."""
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        """Return a normalized version of the vector."""
        mag = self.magnitude()
        if mag == 0:
            return Vector3D(0, 0, 0)
        return Vector3D(self.x/mag, self.y/mag, self.z/mag)

    def __add__(self, other):
        """Add two vectors."""
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        """Subtract two vectors."""
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        """Multiply vector by scalar."""
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar):
        """Multiply vector by scalar (reverse order)."""
        return self.__mul__(scalar)

    def dot(self, other) -> float:
        """Calculate dot product of two vectors."""
        return self.x * other.x + self.y * other.y + self.z * other.z


@dataclass
class PhysicalObject:
    """Represents a physical object in the simulation."""
    object_type: ObjectType
    position: Vector3D
    velocity: Vector3D
    mass: float
    restitution: float = 0.8  # Bounciness (0.0 = no bounce, 1.0 = perfect bounce)
    friction: float = 0.1     # Surface friction
    size: float = 1.0         # For spheres, this is radius; for cubes, this is half-side length
    name: str = ""

    def update_position(self, dt: float):
        """Update position based on velocity."""
        self.position = Vector3D(
            self.position.x + self.velocity.x * dt,
            self.position.y + self.velocity.y * dt,
            self.position.z + self.velocity.z * dt
        )

    def apply_force(self, force: Vector3D, dt: float):
        """Apply a force to the object, changing its velocity."""
        # F = ma, so a = F/m
        acceleration = Vector3D(force.x / self.mass, force.y / self.mass, force.z / self.mass)
        self.velocity = Vector3D(
            self.velocity.x + acceleration.x * dt,
            self.velocity.y + acceleration.y * dt,
            self.velocity.z + acceleration.z * dt
        )

    def kinetic_energy(self) -> float:
        """Calculate the kinetic energy of the object."""
        v_squared = self.velocity.x**2 + self.velocity.y**2 + self.velocity.z**2
        return 0.5 * self.mass * v_squared


class PhysicsEngine:
    """A simple physics engine for simulating basic physical interactions."""

    def __init__(self, gravity: Vector3D = None, time_step: float = 0.01):
        self.objects: List[PhysicalObject] = []
        self.gravity = gravity or Vector3D(0, -9.81, 0)  # Earth gravity
        self.time_step = time_step
        self.time = 0.0

    def add_object(self, obj: PhysicalObject):
        """Add an object to the simulation."""
        self.objects.append(obj)

    def remove_object(self, obj: PhysicalObject):
        """Remove an object from the simulation."""
        if obj in self.objects:
            self.objects.remove(obj)

    def detect_collision(self, obj1: PhysicalObject, obj2: PhysicalObject) -> bool:
        """Detect collision between two objects (simplified for spheres)."""
        if obj1.object_type == ObjectType.SPHERE and obj2.object_type == ObjectType.SPHERE:
            # Distance between centers
            dist_vec = Vector3D(
                obj1.position.x - obj2.position.x,
                obj1.position.y - obj2.position.y,
                obj1.position.z - obj2.position.z
            )
            distance = dist_vec.magnitude()
            min_distance = obj1.size + obj2.size
            return distance < min_distance
        elif obj1.object_type == ObjectType.SPHERE and obj2.object_type == ObjectType.PLANE:
            # Distance from sphere center to plane (simplified)
            # Assuming plane is at y=0 with normal (0,1,0)
            distance = abs(obj1.position.y)
            return distance < obj1.size
        elif obj1.object_type == ObjectType.PLANE and obj2.object_type == ObjectType.SPHERE:
            return self.detect_collision(obj2, obj1)
        return False

    def handle_collision(self, obj1: PhysicalObject, obj2: PhysicalObject):
        """Handle collision response between two objects."""
        if obj1.object_type == ObjectType.SPHERE and obj2.object_type == ObjectType.SPHERE:
            # Simplified sphere-sphere collision
            # Calculate collision normal
            normal = Vector3D(
                obj1.position.x - obj2.position.x,
                obj1.position.y - obj2.position.y,
                obj1.position.z - obj2.position.z
            ).normalize()

            # Calculate relative velocity
            rel_velocity = Vector3D(
                obj1.velocity.x - obj2.velocity.x,
                obj1.velocity.y - obj2.velocity.y,
                obj1.velocity.z - obj2.velocity.z
            )

            # Calculate velocity along normal
            vel_along_normal = rel_velocity.dot(normal)

            # Don't resolve if objects are moving apart
            if vel_along_normal > 0:
                return

            # Calculate restitution (bounciness)
            restitution = min(obj1.restitution, obj2.restitution)

            # Calculate impulse scalar
            impulse_scalar = -(1 + restitution) * vel_along_normal
            impulse_scalar /= (1/obj1.mass + 1/obj2.mass)

            # Apply impulse
            impulse = Vector3D(
                impulse_scalar * normal.x,
                impulse_scalar * normal.y,
                impulse_scalar * normal.z
            )

            obj1.velocity = Vector3D(
                obj1.velocity.x + impulse.x / obj1.mass,
                obj1.velocity.y + impulse.y / obj1.mass,
                obj1.velocity.z + impulse.z / obj1.mass
            )

            obj2.velocity = Vector3D(
                obj2.velocity.x - impulse.x / obj2.mass,
                obj2.velocity.y - impulse.y / obj2.mass,
                obj2.velocity.z - impulse.z / obj2.mass
            )

            # Position correction to prevent sticking
            percent = 0.8  # Penetration percentage to correct
            slop = 0.01    # Slope to ignore
            correction = (max((obj1.size + obj2.size) -
                            Vector3D(obj1.position.x - obj2.position.x,
                                   obj1.position.y - obj2.position.y,
                                   obj1.position.z - obj2.position.z).magnitude(), 0)
                         / (1/obj1.mass + 1/obj2.mass)) * percent

            correction_vector = Vector3D(
                correction * normal.x,
                correction * normal.y,
                correction * normal.z
            )

            obj1.position = Vector3D(
                obj1.position.x + correction_vector.x / obj1.mass,
                obj1.position.y + correction_vector.y / obj1.mass,
                obj1.position.z + correction_vector.z / obj1.mass
            )

            obj2.position = Vector3D(
                obj2.position.x - correction_vector.x / obj2.mass,
                obj2.position.y - correction_vector.y / obj2.mass,
                obj2.position.z - correction_vector.z / obj2.mass
            )

    def update(self):
        """Update the simulation by one time step."""
        # Apply gravity to all objects
        for obj in self.objects:
            if obj.object_type != ObjectType.PLANE:  # Planes don't move
                gravity_force = Vector3D(
                    self.gravity.x * obj.mass,
                    self.gravity.y * obj.mass,
                    self.gravity.z * obj.mass
                )
                obj.apply_force(gravity_force, self.time_step)

        # Update positions
        for obj in self.objects:
            if obj.object_type != ObjectType.PLANE:
                obj.update_position(self.time_step)

        # Handle collisions
        for i in range(len(self.objects)):
            for j in range(i + 1, len(self.objects)):
                obj1, obj2 = self.objects[i], self.objects[j]
                if self.detect_collision(obj1, obj2):
                    self.handle_collision(obj1, obj2)

        # Handle ground collision (assuming ground is at y=0)
        for obj in self.objects:
            if obj.object_type == ObjectType.SPHERE and obj.position.y - obj.size < 0:
                # Collision with ground
                obj.position.y = obj.size  # Move above ground
                # Apply bounce with energy loss
                obj.velocity.y = -obj.velocity.y * obj.restitution
                # Apply friction
                obj.velocity.x *= (1 - obj.friction)
                obj.velocity.z *= (1 - obj.friction)

        self.time += self.time_step


class PhysicsDemo:
    """Main demonstration class for the physics simulation."""

    def __init__(self):
        self.engine = PhysicsEngine()
        self.demo_steps = 0
        self.max_steps = 500  # Run for 5 seconds (500 * 0.01s)

    def setup_scenario(self):
        """Set up the physics scenario with objects."""
        print("Setting up physics scenario...")

        # Add a ground plane
        ground = PhysicalObject(
            object_type=ObjectType.PLANE,
            position=Vector3D(0, 0, 0),
            velocity=Vector3D(0, 0, 0),
            mass=float('inf'),  # Infinite mass for fixed plane
            restitution=0.5,
            friction=0.2,
            size=1.0,
            name="Ground"
        )
        self.engine.add_object(ground)

        # Add a sphere
        sphere1 = PhysicalObject(
            object_type=ObjectType.SPHERE,
            position=Vector3D(0, 10, 0),  # 10m above ground
            velocity=Vector3D(2, 0, 0),   # Moving horizontally
            mass=1.0,
            restitution=0.7,
            friction=0.1,
            size=0.5,  # 0.5m radius
            name="Sphere1"
        )
        self.engine.add_object(sphere1)

        # Add another sphere
        sphere2 = PhysicalObject(
            object_type=ObjectType.SPHERE,
            position=Vector3D(5, 8, 0),   # 8m above ground, 5m away
            velocity=Vector3D(-1, 0, 0),  # Moving toward first sphere
            mass=1.5,
            restitution=0.8,
            friction=0.15,
            size=0.7,  # 0.7m radius
            name="Sphere2"
        )
        self.engine.add_object(sphere2)

        print(f"Added {len(self.engine.objects)} objects to simulation")

    def run_step(self) -> bool:
        """Run one step of the physics simulation."""
        self.engine.update()

        # Print status occasionally
        if self.demo_steps % 50 == 0:
            print(f"\nStep {self.demo_steps} (Time: {self.engine.time:.2f}s):")
            for obj in self.engine.objects:
                if obj.object_type != ObjectType.PLANE:
                    print(f"  {obj.name}: pos=({obj.position.x:.2f}, {obj.position.y:.2f}, {obj.position.z:.2f}), "
                          f"vel=({obj.velocity.x:.2f}, {obj.velocity.y:.2f}, {obj.velocity.z:.2f}), "
                          f"KE={obj.kinetic_energy():.2f}")

        self.demo_steps += 1
        return self.demo_steps < self.max_steps

    def run_demo(self):
        """Run the complete physics simulation demonstration."""
        print("Physical AI Physics Scenario Demo")
        print("=" * 40)
        print("Simulating basic physics principles in Physical AI systems\n")

        # Set up the scenario
        self.setup_scenario()

        print("\nStarting physics simulation...")
        print("Objects will be affected by gravity, collisions, and friction\n")

        start_time = time.time()

        # Run the simulation
        while self.run_step():
            time.sleep(0.001)  # Small delay to make it observable

        elapsed_time = time.time() - start_time

        # Print final results
        print(f"\nDemo completed after {elapsed_time:.2f} seconds")
        print(f"Simulation time: {self.engine.time:.2f} seconds")
        print("\nFinal object states:")
        for obj in self.engine.objects:
            if obj.object_type != ObjectType.PLANE:
                print(f"  {obj.name}: pos=({obj.position.x:.2f}, {obj.position.y:.2f}, {obj.position.z:.2f}), "
                      f"vel=({obj.velocity.x:.2f}, {obj.velocity.y:.2f}, {obj.velocity.z:.2f}), "
                      f"KE={obj.kinetic_energy():.2f}")


def main():
    """Main function to run the physics simulation demonstration."""
    demo = PhysicsDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()