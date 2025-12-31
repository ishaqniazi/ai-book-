"""
Digital World Mapping Example

This script demonstrates how a Physical AI system might create and maintain
a digital representation of its physical environment, connecting physical space
to digital models.
"""

import time
import random
import math
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional, Set
from enum import Enum


class MapObjectType(Enum):
    """Types of objects in the digital map."""
    WALL = "wall"
    OBSTACLE = "obstacle"
    LANDMARK = "landmark"
    PATH = "path"
    GOAL = "goal"


@dataclass
class PhysicalObject:
    """Represents a physical object in the real world."""
    id: str
    x: float  # X coordinate
    y: float  # Y coordinate
    object_type: MapObjectType
    size: float  # Size/dimension
    description: str
    confidence: float = 1.0  # Detection confidence


@dataclass
class DigitalMapCell:
    """Represents a cell in the digital map grid."""
    x: int
    y: int
    object_type: Optional[MapObjectType] = None
    confidence: float = 0.0
    visited: bool = False
    last_updated: float = 0.0


class PhysicalEnvironment:
    """Simulates a physical environment with objects."""

    def __init__(self, width: int = 20, height: int = 20):
        self.width = width
        self.height = height
        self.objects: List[PhysicalObject] = []
        self.robot_x = 0.0
        self.robot_y = 0.0
        self.generate_environment()

    def generate_environment(self):
        """Generate a random environment with objects."""
        # Add some walls
        for x in range(self.width):
            self.objects.append(PhysicalObject(
                id=f"wall_h_{x}_0", x=x, y=0,
                object_type=MapObjectType.WALL, size=1.0,
                description="Horizontal wall"
            ))
            self.objects.append(PhysicalObject(
                id=f"wall_h_{x}_{self.height-1}", x=x, y=self.height-1,
                object_type=MapObjectType.WALL, size=1.0,
                description="Horizontal wall"
            ))

        for y in range(self.height):
            self.objects.append(PhysicalObject(
                id=f"wall_v_0_{y}", x=0, y=y,
                object_type=MapObjectType.WALL, size=1.0,
                description="Vertical wall"
            ))
            self.objects.append(PhysicalObject(
                id=f"wall_v_{self.width-1}_{y}", x=self.width-1, y=y,
                object_type=MapObjectType.WALL, size=1.0,
                description="Vertical wall"
            ))

        # Add some obstacles
        for i in range(5):
            x = random.randint(2, self.width-3)
            y = random.randint(2, self.height-3)
            self.objects.append(PhysicalObject(
                id=f"obs_{i}", x=x, y=y,
                object_type=MapObjectType.OBSTACLE, size=1.0,
                description=f"Obstacle {i}"
            ))

        # Add a landmark
        self.objects.append(PhysicalObject(
            id="landmark_1", x=5, y=5,
            object_type=MapObjectType.LANDMARK, size=0.5,
            description="Red landmark"
        ))

        # Add a goal
        self.objects.append(PhysicalObject(
            id="goal_1", x=self.width-2, y=self.height-2,
            object_type=MapObjectType.GOAL, size=0.8,
            description="Goal location"
        ))

    def get_objects_in_range(self, x: float, y: float, range_: float) -> List[PhysicalObject]:
        """Get objects within a certain range of the given position."""
        nearby_objects = []
        for obj in self.objects:
            distance = math.sqrt((obj.x - x)**2 + (obj.y - y)**2)
            if distance <= range_:
                # Add some randomness to detection
                detection_prob = max(0.1, 1.0 - distance/range_)  # Better detection closer
                if random.random() < detection_prob:
                    # Add detection uncertainty
                    confidence = min(1.0, detection_prob + random.uniform(-0.1, 0.2))
                    nearby_objects.append(PhysicalObject(
                        id=obj.id,
                        x=obj.x + random.uniform(-0.1, 0.1),  # Add position noise
                        y=obj.y + random.uniform(-0.1, 0.1),
                        object_type=obj.object_type,
                        size=obj.size,
                        description=obj.description,
                        confidence=max(0.0, confidence)
                    ))
        return nearby_objects

    def move_robot(self, new_x: float, new_y: float):
        """Move the robot to a new position."""
        self.robot_x = max(0, min(self.width-1, new_x))
        self.robot_y = max(0, min(self.height-1, new_y))


class DigitalWorldMap:
    """Maintains the digital representation of the physical world."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid: List[List[DigitalMapCell]] = []
        self.physical_to_digital: Dict[str, Tuple[int, int]] = {}  # Physical object ID to grid position
        self.confidence_map: Dict[str, float] = {}  # Object ID to confidence
        self.initialize_grid()

    def initialize_grid(self):
        """Initialize the digital map grid."""
        self.grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(DigitalMapCell(x=x, y=y))
            self.grid.append(row)

    def update_from_physical_objects(self, objects: List[PhysicalObject], robot_x: float, robot_y: float):
        """Update the digital map based on physical object detections."""
        for obj in objects:
            # Convert physical coordinates to grid coordinates
            grid_x = int(round(obj.x))
            grid_y = int(round(obj.y))

            # Check bounds
            if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
                # Update the grid cell
                cell = self.grid[grid_y][grid_x]
                cell.object_type = obj.object_type
                cell.confidence = max(cell.confidence, obj.confidence)
                cell.visited = True
                cell.last_updated = time.time()

                # Update object tracking
                self.physical_to_digital[obj.id] = (grid_x, grid_y)
                self.confidence_map[obj.id] = obj.confidence

    def get_cell(self, x: int, y: int) -> Optional[DigitalMapCell]:
        """Get a cell from the grid."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Get valid neighboring cells."""
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # 4-connected
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbors.append((nx, ny))
        return neighbors

    def get_path_to_goal(self, start_x: int, start_y: int) -> Optional[List[Tuple[int, int]]]:
        """Simple pathfinding to the goal using BFS."""
        # Find goal location
        goal_pos = None
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x].object_type == MapObjectType.GOAL:
                    goal_pos = (x, y)
                    break
            if goal_pos:
                break

        if not goal_pos:
            return None

        # BFS for pathfinding
        queue = [(start_x, start_y, [(start_x, start_y)])]
        visited = {(start_x, start_y)}

        while queue:
            x, y, path = queue.pop(0)

            if (x, y) == goal_pos:
                return path

            for nx, ny in self.get_neighbors(x, y):
                if (nx, ny) not in visited:
                    cell = self.grid[ny][nx]
                    # Only move to cells that aren't obstacles or walls
                    if cell.object_type not in [MapObjectType.OBSTACLE, MapObjectType.WALL]:
                        visited.add((nx, ny))
                        new_path = path + [(nx, ny)]
                        queue.append((nx, ny, new_path))

        return None  # No path found

    def print_map(self, robot_x: int, robot_y: int):
        """Print a visual representation of the map."""
        print("\nDigital World Map:")
        print("  " + " ".join([str(i % 10) for i in range(self.width)]))

        for y in range(self.height):
            row_str = f"{y % 10} "
            for x in range(self.width):
                cell = self.grid[y][x]
                if x == robot_x and y == robot_y:
                    row_str += "R "  # Robot position
                elif cell.object_type == MapObjectType.WALL:
                    row_str += "# "  # Wall
                elif cell.object_type == MapObjectType.OBSTACLE:
                    row_str += "O "  # Obstacle
                elif cell.object_type == MapObjectType.LANDMARK:
                    row_str += "L "  # Landmark
                elif cell.object_type == MapObjectType.GOAL:
                    row_str += "G "  # Goal
                elif cell.visited:
                    row_str += ". "  # Explored
                else:
                    row_str += "? "  # Unknown
            print(row_str)
        print()


class WorldMapper:
    """Manages the mapping process between physical and digital worlds."""

    def __init__(self, env_width: int, env_height: int):
        self.physical_env = PhysicalEnvironment(env_width, env_height)
        self.digital_map = DigitalWorldMap(env_width, env_height)
        self.sensing_range = 3.0
        self.mapping_history: List[Dict] = []

    def explore_step(self) -> bool:
        """Perform one exploration step."""
        # Get current robot position
        robot_x, robot_y = self.physical_env.robot_x, self.physical_env.robot_y

        # Sense nearby objects
        nearby_objects = self.physical_env.get_objects_in_range(
            robot_x, robot_y, self.sensing_range
        )

        # Update digital map
        self.digital_map.update_from_physical_objects(nearby_objects, robot_x, robot_y)

        # Store mapping history
        history_entry = {
            "timestamp": time.time(),
            "robot_position": (robot_x, robot_y),
            "objects_detected": len(nearby_objects),
            "map_coverage": self.get_map_coverage()
        }
        self.mapping_history.append(history_entry)

        # Simple exploration strategy: move toward unexplored areas
        self.move_robot_intelligently()

        return True

    def move_robot_intelligently(self):
        """Move robot to explore more of the environment."""
        current_x, current_y = self.physical_env.robot_x, self.physical_env.robot_y

        # Look for unexplored areas nearby
        best_move = None
        best_score = -1

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  # Skip current position

                new_x = current_x + dx
                new_y = current_y + dy

                # Check bounds
                if 0 <= new_x < self.physical_env.width and 0 <= new_y < self.physical_env.height:
                    cell = self.digital_map.get_cell(int(new_x), int(new_y))
                    if cell:
                        # Prefer unvisited cells, but also consider low-confidence cells
                        score = 0
                        if not cell.visited:
                            score += 10  # High priority for unvisited
                        if cell.confidence < 0.5:
                            score += 5  # Medium priority for low confidence
                        if cell.object_type == MapObjectType.LANDMARK:
                            score += 3  # Bonus for landmarks

                        if score > best_score:
                            best_score = score
                            best_move = (new_x, new_y)

        # If we found a good move, take it
        if best_move:
            self.physical_env.move_robot(best_move[0], best_move[1])
        else:
            # Otherwise, make a random move
            new_x = current_x + random.uniform(-1, 1)
            new_y = current_y + random.uniform(-1, 1)
            self.physical_env.move_robot(new_x, new_y)

    def get_map_coverage(self) -> float:
        """Calculate the percentage of map that has been explored."""
        total_cells = self.digital_map.width * self.digital_map.height
        visited_cells = sum(
            1 for row in self.digital_map.grid for cell in row if cell.visited
        )
        return visited_cells / total_cells if total_cells > 0 else 0.0

    def get_mapping_statistics(self) -> Dict:
        """Get statistics about the mapping process."""
        if not self.mapping_history:
            return {
                "map_coverage": 0.0,
                "objects_mapped": 0,
                "exploration_steps": 0,
                "average_confidence": 0.0
            }

        # Count unique objects mapped
        mapped_objects = set()
        total_confidence = 0.0
        confidence_count = 0

        for y in range(self.digital_map.height):
            for x in range(self.digital_map.width):
                cell = self.digital_map.grid[y][x]
                if cell.visited and cell.object_type:
                    mapped_objects.add((x, y, cell.object_type))
                    total_confidence += cell.confidence
                    confidence_count += 1

        avg_confidence = total_confidence / confidence_count if confidence_count > 0 else 0.0

        return {
            "map_coverage": self.get_map_coverage(),
            "objects_mapped": len(mapped_objects),
            "exploration_steps": len(self.mapping_history),
            "average_confidence": avg_confidence
        }


class DigitalMappingDemo:
    """Main demonstration class for digital world mapping."""

    def __init__(self):
        self.mapper = WorldMapper(15, 15)  # 15x15 environment
        self.demo_steps = 0
        self.max_steps = 30  # Run for 30 steps

    def run_step(self) -> bool:
        """Run one step of the mapping simulation."""
        print(f"\n--- Mapping Step {self.demo_steps + 1} ---")

        # Perform exploration step
        self.mapper.explore_step()

        # Print current status
        stats = self.mapper.get_mapping_statistics()
        robot_x, robot_y = int(self.mapper.physical_env.robot_x), int(self.mapper.physical_env.robot_y)

        print(f"Robot position: ({robot_x}, {robot_y})")
        print(f"Map coverage: {stats['map_coverage']:.1%}")
        print(f"Objects mapped: {stats['objects_mapped']}")
        print(f"Average confidence: {stats['average_confidence']:.2f}")

        # Print map occasionally
        if self.demo_steps % 10 == 0:
            self.mapper.digital_map.print_map(robot_x, robot_y)

        self.demo_steps += 1
        return self.demo_steps < self.max_steps

    def run_demo(self):
        """Run the complete digital mapping demonstration."""
        print("Physical AI Digital World Mapping Demo")
        print("=" * 50)
        print("Simulating mapping of physical environment to digital representation\n")

        start_time = time.time()

        # Run the simulation
        while self.run_step():
            time.sleep(0.1)  # Small delay to make it observable

        elapsed_time = time.time() - start_time

        # Print final map
        robot_x, robot_y = int(self.mapper.physical_env.robot_x), int(self.mapper.physical_env.robot_y)
        print(f"\nFinal Map:")
        self.mapper.digital_map.print_map(robot_x, robot_y)

        # Print final statistics
        stats = self.mapper.get_mapping_statistics()

        print(f"\nDemo completed after {elapsed_time:.2f} seconds")
        print(f"\nFinal Mapping Statistics:")
        print(f"  Map Coverage: {stats['map_coverage']:.1%}")
        print(f"  Objects Mapped: {stats['objects_mapped']}")
        print(f"  Exploration Steps: {stats['exploration_steps']}")
        print(f"  Average Confidence: {stats['average_confidence']:.2f}")

        # Show path planning example
        path = self.mapper.digital_map.get_path_to_goal(robot_x, robot_y)
        if path:
            print(f"  Path to goal found: {len(path)} steps")
        else:
            print(f"  No path to goal found")


def main():
    """Main function to run the digital mapping demonstration."""
    demo = DigitalMappingDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()