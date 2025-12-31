"""
Pseudo Mapping Example

This script demonstrates basic concepts of environmental mapping for robotics.
It simulates how a robot can build a map of its environment using sensor data,
representing space in different ways for navigation and understanding.
"""

import time
import random
import math
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
from enum import Enum


class MapType(Enum):
    """Types of maps a robot can create."""
    OCCUPANCY_GRID = "occupancy_grid"
    TOPOLOGICAL = "topological"
    FEATURE_BASED = "feature_based"
    METRIC = "metric"


class CellType(Enum):
    """Types of cells in a grid map."""
    FREE = "free"
    OCCUPIED = "occupied"
    UNKNOWN = "unknown"
    OBSTACLE = "obstacle"


@dataclass
class MapCell:
    """Represents a cell in a grid map."""
    x: int
    y: int
    cell_type: CellType
    occupancy_probability: float = 0.0  # 0.0 = definitely free, 1.0 = definitely occupied
    confidence: float = 0.0  # Confidence in the cell's state


@dataclass
class MapFeature:
    """Represents a feature in the environment."""
    id: str
    position: Tuple[float, float, float]  # x, y, z coordinates
    feature_type: str  # landmark, object, etc.
    confidence: float = 1.0


@dataclass
class TopologicalNode:
    """Represents a node in a topological map."""
    id: str
    position: Tuple[float, float]  # x, y coordinates
    connections: List[str]  # IDs of connected nodes
    description: str


class OccupancyGridMap:
    """Represents an occupancy grid map."""

    def __init__(self, width: int, height: int, resolution: float = 1.0):
        self.width = width
        self.height = height
        self.resolution = resolution  # meters per cell
        self.grid: List[List[MapCell]] = self._initialize_grid()

    def _initialize_grid(self) -> List[List[MapCell]]:
        """Initialize an empty grid."""
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(MapCell(
                    x=x, y=y, cell_type=CellType.UNKNOWN,
                    occupancy_probability=0.5, confidence=0.0
                ))
            grid.append(row)
        return grid

    def update_cell(self, x: int, y: int, occupancy_prob: float, confidence: float = 1.0):
        """Update a cell with new occupancy information."""
        if 0 <= x < self.width and 0 <= y < self.height:
            cell = self.grid[y][x]
            # Update occupancy probability using simple averaging
            old_prob = cell.occupancy_probability
            old_conf = cell.confidence

            new_prob = (old_prob * old_conf + occupancy_prob * confidence) / (old_conf + confidence)
            new_conf = min(1.0, old_conf + confidence)

            cell.occupancy_probability = new_prob
            cell.confidence = new_conf

            # Update cell type based on probability
            if new_prob > 0.7:
                cell.cell_type = CellType.OCCUPIED
            elif new_prob < 0.3:
                cell.cell_type = CellType.FREE
            else:
                cell.cell_type = CellType.UNKNOWN

    def get_cell(self, x: int, y: int) -> Optional[MapCell]:
        """Get a cell at specific coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def get_occupancy_probability(self, x: int, y: int) -> float:
        """Get occupancy probability at specific coordinates."""
        cell = self.get_cell(x, y)
        return cell.occupancy_probability if cell else 0.5

    def get_free_space(self) -> List[Tuple[int, int]]:
        """Get coordinates of free space cells."""
        free_cells = []
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x].cell_type == CellType.FREE:
                    free_cells.append((x, y))
        return free_cells

    def get_obstacles(self) -> List[Tuple[int, int]]:
        """Get coordinates of obstacle cells."""
        obstacle_cells = []
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x].cell_type in [CellType.OCCUPIED, CellType.OBSTACLE]:
                    obstacle_cells.append((x, y))
        return obstacle_cells


class FeatureBasedMap:
    """Represents a feature-based map."""

    def __init__(self):
        self.features: List[MapFeature] = []
        self.feature_descriptors: Dict[str, List[float]] = {}

    def add_feature(self, feature: MapFeature):
        """Add a feature to the map."""
        self.features.append(feature)
        # Generate a simple descriptor for the feature
        self.feature_descriptors[feature.id] = [
            feature.position[0], feature.position[1], feature.position[2],
            hash(feature.feature_type) % 1000 / 1000.0
        ]

    def find_feature_by_type(self, feature_type: str) -> List[MapFeature]:
        """Find features of a specific type."""
        return [f for f in self.features if f.feature_type == feature_type]

    def get_nearest_feature(self, position: Tuple[float, float, float]) -> Optional[MapFeature]:
        """Find the nearest feature to a given position."""
        if not self.features:
            return None

        nearest = None
        min_dist = float('inf')

        for feature in self.features:
            dist = math.sqrt(
                (feature.position[0] - position[0])**2 +
                (feature.position[1] - position[1])**2 +
                (feature.position[2] - position[2])**2
            )
            if dist < min_dist:
                min_dist = dist
                nearest = feature

        return nearest

    def match_features(self, query_descriptor: List[float], threshold: float = 0.3) -> List[MapFeature]:
        """Match features based on descriptor similarity."""
        matches = []
        for feature_id, descriptor in self.feature_descriptors.items():
            # Simple Euclidean distance for descriptor matching
            dist = math.sqrt(sum((a - b)**2 for a, b in zip(query_descriptor, descriptor)))
            if dist < threshold:
                feature = next((f for f in self.features if f.id == feature_id), None)
                if feature:
                    matches.append(feature)
        return matches


class TopologicalMap:
    """Represents a topological map."""

    def __init__(self):
        self.nodes: Dict[str, TopologicalNode] = {}

    def add_node(self, node: TopologicalNode):
        """Add a node to the topological map."""
        self.nodes[node.id] = node

    def connect_nodes(self, node1_id: str, node2_id: str):
        """Connect two nodes in the topological map."""
        if node1_id in self.nodes and node2_id in self.nodes:
            if node2_id not in self.nodes[node1_id].connections:
                self.nodes[node1_id].connections.append(node2_id)
            if node1_id not in self.nodes[node2_id].connections:
                self.nodes[node2_id].connections.append(node1_id)

    def get_path(self, start_id: str, end_id: str) -> List[str]:
        """Find a path between two nodes using simple BFS."""
        if start_id not in self.nodes or end_id not in self.nodes:
            return []

        if start_id == end_id:
            return [start_id]

        # Simple BFS for path finding
        queue = [(start_id, [start_id])]
        visited = {start_id}

        while queue:
            current_id, path = queue.pop(0)

            for neighbor_id in self.nodes[current_id].connections:
                if neighbor_id == end_id:
                    return path + [neighbor_id]

                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    queue.append((neighbor_id, path + [neighbor_id]))

        return []  # No path found


class PseudoMapper:
    """Main mapping system that combines different mapping approaches."""

    def __init__(self, grid_width: int = 20, grid_height: int = 20):
        self.occupancy_map = OccupancyGridMap(grid_width, grid_height)
        self.feature_map = FeatureBasedMap()
        self.topological_map = TopologicalMap()
        self.robot_position = (0, 0, 0)  # x, y, z
        self.map_history: List[Dict] = []

    def update_from_sensor_data(self, sensor_readings: List[Tuple[float, float, float, bool]]):
        """
        Update the map based on sensor readings.
        Each reading is (x, y, z, is_occupied) in robot's coordinate system.
        """
        for x, y, z, is_occupied in sensor_readings:
            # Convert to map coordinates (simplified)
            map_x = int(x + self.occupancy_map.width // 2)
            map_y = int(y + self.occupancy_map.height // 2)

            if 0 <= map_x < self.occupancy_map.width and 0 <= map_y < self.occupancy_map.height:
                occupancy_prob = 0.9 if is_occupied else 0.1
                confidence = 0.8  # High confidence in sensor readings
                self.occupancy_map.update_cell(map_x, map_y, occupancy_prob, confidence)

    def add_landmark(self, position: Tuple[float, float, float], landmark_type: str):
        """Add a landmark to the feature map."""
        feature = MapFeature(
            id=f"landmark_{len(self.feature_map.features)}",
            position=position,
            feature_type=landmark_type,
            confidence=0.9
        )
        self.feature_map.add_feature(feature)

    def update_robot_position(self, new_position: Tuple[float, float, float]):
        """Update the robot's position in the world."""
        self.robot_position = new_position

    def build_topological_map(self):
        """Build a topological map from the occupancy grid."""
        # Find free spaces that could be waypoints
        free_spaces = self.occupancy_map.get_free_space()
        if not free_spaces:
            return

        # Create nodes for interesting locations
        node_positions = []
        for i in range(0, len(free_spaces), 5):  # Sample every 5th free cell
            x, y = free_spaces[i]
            node_positions.append((float(x), float(y)))

        # Create nodes
        for i, pos in enumerate(node_positions):
            node = TopologicalNode(
                id=f"waypoint_{i}",
                position=pos,
                connections=[],
                description=f"Free space at ({pos[0]}, {pos[1]})"
            )
            self.topological_map.add_node(node)

        # Connect nearby nodes
        node_ids = list(self.topological_map.nodes.keys())
        for i, node_id1 in enumerate(node_ids):
            for j, node_id2 in enumerate(node_ids[i+1:], i+1):
                pos1 = self.topological_map.nodes[node_id1].position
                pos2 = self.topological_map.nodes[node_id2].position
                dist = math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
                if dist < 3.0:  # Connect if closer than 3 units
                    self.topological_map.connect_nodes(node_id1, node_id2)

    def get_map_summary(self) -> Dict:
        """Get a summary of the current map state."""
        free_cells = len(self.occupancy_map.get_free_space())
        obstacle_cells = len(self.occupancy_map.get_obstacles())
        total_cells = self.occupancy_map.width * self.occupancy_map.height

        return {
            'occupancy_map': {
                'dimensions': (self.occupancy_map.width, self.occupancy_map.height),
                'free_cells': free_cells,
                'obstacle_cells': obstacle_cells,
                'occupancy_rate': obstacle_cells / total_cells if total_cells > 0 else 0
            },
            'feature_map': {
                'total_features': len(self.feature_map.features),
                'feature_types': list(set(f.feature_type for f in self.feature_map.features))
            },
            'topological_map': {
                'total_nodes': len(self.topological_map.nodes),
                'total_connections': sum(len(node.connections) for node in self.topological_map.nodes.values())
            }
        }


class MappingDemo:
    """Main demonstration class for mapping system."""

    def __init__(self):
        self.mapper = PseudoMapper()
        self.demo_step = 0
        self.max_steps = 8

    def generate_simulated_sensor_data(self) -> List[Tuple[float, float, float, bool]]:
        """Generate simulated sensor readings."""
        readings = []
        # Generate some obstacles in a pattern
        for i in range(10):
            x = random.uniform(-8, 8)
            y = random.uniform(-8, 8)
            z = 0.0
            is_occupied = random.random() > 0.7  # 30% chance of being occupied
            readings.append((x, y, z, is_occupied))

        # Add some structure (e.g., walls)
        for i in range(5):
            # Horizontal wall
            readings.append((float(i - 2), -5.0, 0.0, True))
            # Vertical wall
            readings.append((-7.0, float(i - 2), 0.0, True))

        return readings

    def run_mapping_step(self) -> bool:
        """Run one step of mapping."""
        print(f"\n--- Mapping Step {self.demo_step + 1} ---")

        # Generate simulated sensor data
        sensor_data = self.generate_simulated_sensor_data()
        print(f"Received {len(sensor_data)} sensor readings")

        # Update the map with sensor data
        self.mapper.update_from_sensor_data(sensor_data)

        # Add some landmarks
        if self.demo_step % 3 == 0:
            landmark_pos = (random.uniform(-5, 5), random.uniform(-5, 5), 0.0)
            self.mapper.add_landmark(landmark_pos, "landmark")

        # Update robot position
        new_pos = (random.uniform(-10, 10), random.uniform(-10, 10), 0.0)
        self.mapper.update_robot_position(new_pos)

        # Build topological map periodically
        if self.demo_step % 4 == 0:
            self.mapper.build_topological_map()

        # Get and display map summary
        summary = self.mapper.get_map_summary()
        print(f"Map summary:")
        print(f"  Occupancy: {summary['occupancy_map']['free_cells']} free, "
              f"{summary['occupancy_map']['obstacle_cells']} obstacles")
        print(f"  Features: {summary['feature_map']['total_features']} landmarks")
        print(f"  Topology: {summary['topological_map']['total_nodes']} nodes, "
              f"{summary['topological_map']['total_connections']} connections")

        self.demo_step += 1
        return self.demo_step < self.max_steps

    def run_demo(self):
        """Run the complete mapping demonstration."""
        print("Pseudo Mapping Simulation Demo")
        print("=" * 30)
        print("Simulating how a robot builds a map of its environment using sensor data.")
        print("The system creates multiple types of maps: occupancy grids, feature maps,")
        print("and topological maps for different navigation and understanding purposes.\n")

        print("Mapping approaches demonstrated:")
        print("- Occupancy grid mapping (probabilistic representation)")
        print("- Feature-based mapping (landmark identification)")
        print("- Topological mapping (waypoint and path planning)\n")

        # Run the mapping simulation
        while self.run_mapping_step():
            time.sleep(0.5)  # Simulate processing time

        print(f"\nDemo completed after {self.demo_step} mapping steps")

        # Final summary
        final_summary = self.mapper.get_map_summary()
        print(f"\nFinal Map Summary:")
        for map_type, details in final_summary.items():
            print(f"  {map_type}:")
            for key, value in details.items():
                print(f"    {key}: {value}")


def main():
    """Main function to run the mapping simulation."""
    demo = MappingDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()