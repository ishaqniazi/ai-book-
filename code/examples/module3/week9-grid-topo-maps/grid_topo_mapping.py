"""
Grid and Topological Mapping Example

This script demonstrates concepts of grid-based and topological mapping for robotics.
It shows how robots can represent their environment using both metric (grid) and
topological (waypoint-based) approaches for navigation and spatial understanding.
"""

import time
import random
import math
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional, Set
from enum import Enum


class MapCellType(Enum):
    """Types of cells in a grid map."""
    FREE = "free"
    OCCUPIED = "occupied"
    UNKNOWN = "unknown"
    DOOR = "door"
    STAIRS = "stairs"
    ELEVATOR = "elevator"


class TopologicalNodeType(Enum):
    """Types of nodes in a topological map."""
    ROOM = "room"
    CORRIDOR = "corridor"
    DOORWAY = "doorway"
    STAIRCASE = "staircase"
    ELEVATOR = "elevator"
    LANDMARK = "landmark"


@dataclass
class GridCell:
    """Represents a cell in a grid map."""
    x: int
    y: int
    cell_type: MapCellType
    occupancy_probability: float  # 0.0 = free, 1.0 = occupied
    traversable: bool = True
    visited: bool = False


@dataclass
class TopologicalNode:
    """Represents a node in a topological map."""
    id: str
    name: str
    position: Tuple[float, float]  # x, y coordinates in the grid
    node_type: TopologicalNodeType
    connections: List[str]  # IDs of connected nodes
    description: str = ""


class GridMap:
    """Represents a metric grid map of the environment."""

    def __init__(self, width: int, height: int, resolution: float = 0.5):
        self.width = width
        self.height = height
        self.resolution = resolution  # meters per cell
        self.grid: List[List[GridCell]] = self._initialize_grid()

    def _initialize_grid(self) -> List[List[GridCell]]:
        """Initialize an empty grid."""
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(GridCell(
                    x=x, y=y,
                    cell_type=MapCellType.UNKNOWN,
                    occupancy_probability=0.5,
                    traversable=True,
                    visited=False
                ))
            grid.append(row)
        return grid

    def set_cell(self, x: int, y: int, cell_type: MapCellType, occupancy_prob: float = 0.5):
        """Set the properties of a specific cell."""
        if 0 <= x < self.width and 0 <= y < self.height:
            cell = self.grid[y][x]
            cell.cell_type = cell_type
            cell.occupancy_probability = occupancy_prob
            cell.traversable = cell_type != MapCellType.OCCUPIED
            cell.visited = True

    def get_cell(self, x: int, y: int) -> Optional[GridCell]:
        """Get a specific cell."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def is_traversable(self, x: int, y: int) -> bool:
        """Check if a cell is traversable."""
        cell = self.get_cell(x, y)
        return cell.traversable if cell else False

    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Get traversable neighbor cells."""
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1),  # 4-connectivity
                        (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # 8-connectivity
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height and self.is_traversable(nx, ny):
                neighbors.append((nx, ny))
        return neighbors

    def get_free_space(self) -> List[Tuple[int, int]]:
        """Get coordinates of free space cells."""
        free_cells = []
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x].cell_type == MapCellType.FREE:
                    free_cells.append((x, y))
        return free_cells

    def get_special_cells(self, cell_type: MapCellType) -> List[Tuple[int, int]]:
        """Get coordinates of cells of a specific type."""
        cells = []
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x].cell_type == cell_type:
                    cells.append((x, y))
        return cells

    def calculate_distance(self, start: Tuple[int, int], goal: Tuple[int, int]) -> float:
        """Calculate Euclidean distance between two points."""
        dx = start[0] - goal[0]
        dy = start[1] - goal[1]
        return math.sqrt(dx*dx + dy*dy)


class TopologicalMap:
    """Represents a topological map of the environment."""

    def __init__(self):
        self.nodes: Dict[str, TopologicalNode] = {}
        self.node_counter = 0

    def add_node(self, name: str, position: Tuple[float, float], node_type: TopologicalNodeType,
                 description: str = "") -> str:
        """Add a node to the topological map and return its ID."""
        node_id = f"node_{self.node_counter}"
        self.node_counter += 1

        node = TopologicalNode(
            id=node_id,
            name=name,
            position=position,
            node_type=node_type,
            connections=[],
            description=description
        )
        self.nodes[node_id] = node
        return node_id

    def connect_nodes(self, node1_id: str, node2_id: str):
        """Connect two nodes in the topological map."""
        if node1_id in self.nodes and node2_id in self.nodes:
            if node2_id not in self.nodes[node1_id].connections:
                self.nodes[node1_id].connections.append(node2_id)
            if node1_id not in self.nodes[node2_id].connections:
                self.nodes[node2_id].connections.append(node1_id)

    def get_path(self, start_id: str, goal_id: str) -> List[str]:
        """Find a path between two nodes using A* algorithm."""
        if start_id not in self.nodes or goal_id not in self.nodes:
            return []

        if start_id == goal_id:
            return [start_id]

        # Simple A* implementation for topological map
        open_set = {start_id}
        came_from: Dict[str, str] = {}
        g_score: Dict[str, float] = {start_id: 0}
        f_score: Dict[str, float] = {start_id: self._heuristic(start_id, goal_id)}

        while open_set:
            current = min(open_set, key=lambda x: f_score.get(x, float('inf')))

            if current == goal_id:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start_id)
                return path[::-1]

            open_set.remove(current)

            for neighbor_id in self.nodes[current].connections:
                tentative_g_score = g_score[current] + 1  # Simple uniform cost

                if neighbor_id not in g_score or tentative_g_score < g_score[neighbor_id]:
                    came_from[neighbor_id] = current
                    g_score[neighbor_id] = tentative_g_score
                    f_score[neighbor_id] = g_score[neighbor_id] + self._heuristic(neighbor_id, goal_id)
                    open_set.add(neighbor_id)

        return []  # No path found

    def _heuristic(self, node_id1: str, node_id2: str) -> float:
        """Heuristic function for A* (Euclidean distance between node positions)."""
        pos1 = self.nodes[node_id1].position
        pos2 = self.nodes[node_id2].position
        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        return math.sqrt(dx*dx + dy*dy)

    def get_nodes_by_type(self, node_type: TopologicalNodeType) -> List[TopologicalNode]:
        """Get all nodes of a specific type."""
        return [node for node in self.nodes.values() if node.node_type == node_type]

    def get_node_connections(self, node_id: str) -> List[str]:
        """Get connections for a specific node."""
        if node_id in self.nodes:
            return self.nodes[node_id].connections
        return []


class GridTopoMapper:
    """Combines grid and topological mapping approaches."""

    def __init__(self, grid_width: int = 30, grid_height: int = 30):
        self.grid_map = GridMap(grid_width, grid_height)
        self.topological_map = TopologicalMap()
        self.grid_to_topo: Dict[Tuple[int, int], str] = {}  # Maps grid cells to topological nodes
        self.topo_to_grid: Dict[str, Tuple[int, int]] = {}  # Maps topological nodes to grid cells

    def update_grid_from_sensor(self, x: int, y: int, is_occupied: bool, cell_type: MapCellType = MapCellType.FREE):
        """Update grid map based on sensor reading."""
        occupancy_prob = 0.9 if is_occupied else 0.1
        new_cell_type = MapCellType.OCCUPIED if is_occupied else cell_type
        self.grid_map.set_cell(x, y, new_cell_type, occupancy_prob)

    def extract_topological_features(self):
        """Extract topological features from the grid map."""
        # Clear previous mappings
        self.grid_to_topo.clear()
        self.topo_to_grid.clear()

        # Find special cells that could be topological nodes
        door_cells = self.grid_map.get_special_cells(MapCellType.DOOR)
        elevator_cells = self.grid_map.get_special_cells(MapCellType.ELEVATOR)
        stairs_cells = self.grid_map.get_special_cells(MapCellType.STAIRS)

        # Create nodes for special features
        for x, y in door_cells:
            node_id = self.topological_map.add_node(
                f"Door_{x}_{y}",
                (float(x), float(y)),
                TopologicalNodeType.DOORWAY,
                f"Door at ({x}, {y})"
            )
            self.grid_to_topo[(x, y)] = node_id
            self.topo_to_grid[node_id] = (x, y)

        for x, y in elevator_cells:
            node_id = self.topological_map.add_node(
                f"Elevator_{x}_{y}",
                (float(x), float(y)),
                TopologicalNodeType.ELEVATOR,
                f"Elevator at ({x}, {y})"
            )
            self.grid_to_topo[(x, y)] = node_id
            self.topo_to_grid[node_id] = (x, y)

        for x, y in stairs_cells:
            node_id = self.topological_map.add_node(
                f"Stairs_{x}_{y}",
                (float(x), float(y)),
                TopologicalNodeType.STAIRCASE,
                f"Stairs at ({x}, {y})"
            )
            self.grid_to_topo[(x, y)] = node_id
            self.topo_to_grid[node_id] = (x, y)

        # Create room nodes based on connected free space regions
        self._create_room_nodes()

        # Connect nearby nodes
        self._connect_nodes()

    def _create_room_nodes(self):
        """Create room nodes based on connected free space regions."""
        free_cells = self.grid_map.get_free_space()
        visited: Set[Tuple[int, int]] = set()
        room_counter = 0

        for x, y in free_cells:
            if (x, y) not in visited:
                # Find connected component using BFS
                room_cells = self._get_connected_component(x, y)
                visited.update(room_cells)

                # Create a room node at the center of the connected component
                if len(room_cells) > 5:  # Only create room for large enough areas
                    center_x = sum(c[0] for c in room_cells) / len(room_cells)
                    center_y = sum(c[1] for c in room_cells) / len(room_cells)

                    node_id = self.topological_map.add_node(
                        f"Room_{room_counter}",
                        (center_x, center_y),
                        TopologicalNodeType.ROOM,
                        f"Room with {len(room_cells)} cells"
                    )
                    self.topo_to_grid[node_id] = (int(center_x), int(center_y))

                    # Map all cells in this room to this node
                    for cell in room_cells:
                        self.grid_to_topo[cell] = node_id

                    room_counter += 1

    def _get_connected_component(self, start_x: int, start_y: int) -> List[Tuple[int, int]]:
        """Get all connected free cells starting from a given cell."""
        if not self.grid_map.is_traversable(start_x, start_y):
            return []

        component = []
        queue = [(start_x, start_y)]
        visited: Set[Tuple[int, int]] = set()

        while queue:
            x, y = queue.pop(0)
            if (x, y) in visited:
                continue

            visited.add((x, y))
            component.append((x, y))

            for nx, ny in self.grid_map.get_neighbors(x, y):
                if (nx, ny) not in visited and self.grid_map.is_traversable(nx, ny):
                    queue.append((nx, ny))

        return component

    def _connect_nodes(self):
        """Connect nearby topological nodes."""
        node_positions = [(node_id, node.position) for node_id, node in self.topological_map.nodes.items()]

        for i, (node1_id, pos1) in enumerate(node_positions):
            for j, (node2_id, pos2) in enumerate(node_positions[i+1:], i+1):
                # Connect nodes that are close to each other
                distance = math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
                if distance < 5.0:  # Connect if closer than 5 grid units
                    self.topological_map.connect_nodes(node1_id, node2_id)

    def plan_path_grid(self, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Plan a path using the grid map (simplified - in a real system this would use A* or Dijkstra)."""
        # This is a simplified path planning - in a real system you'd use A* or Dijkstra
        path = [start]
        current = start

        while current != goal:
            # Simple greedy approach toward goal
            neighbors = self.grid_map.get_neighbors(current[0], current[1])
            if not neighbors:
                break  # No path possible

            # Find neighbor closest to goal
            best_neighbor = min(neighbors, key=lambda n: self.grid_map.calculate_distance(n, goal))
            path.append(best_neighbor)
            current = best_neighbor

            # Safety check to prevent infinite loops
            if len(path) > 100:
                break

        return path

    def plan_path_topological(self, start_node_id: str, goal_node_id: str) -> List[str]:
        """Plan a path using the topological map."""
        return self.topological_map.get_path(start_node_id, goal_node_id)

    def get_map_summary(self) -> Dict:
        """Get a summary of both map representations."""
        return {
            'grid_map': {
                'dimensions': (self.grid_map.width, self.grid_map.height),
                'total_cells': self.grid_map.width * self.grid_map.height,
                'free_cells': len(self.grid_map.get_free_space()),
                'special_features': {
                    'doors': len(self.grid_map.get_special_cells(MapCellType.DOOR)),
                    'elevators': len(self.grid_map.get_special_cells(MapCellType.ELEVATOR)),
                    'stairs': len(self.grid_map.get_special_cells(MapCellType.STAIRS))
                }
            },
            'topological_map': {
                'total_nodes': len(self.topological_map.nodes),
                'node_types': {
                    node_type.value: len(self.topological_map.get_nodes_by_type(node_type))
                    for node_type in TopologicalNodeType
                },
                'total_connections': sum(len(node.connections) for node in self.topological_map.nodes.values())
            }
        }


class GridTopoMappingDemo:
    """Main demonstration class for grid and topological mapping."""

    def __init__(self):
        self.mapper = GridTopoMapper()
        self.demo_step = 0
        self.max_steps = 10

    def generate_simulated_environment(self):
        """Generate a simulated environment with obstacles and features."""
        # Create some walls
        for x in range(5, 25):
            self.mapper.update_grid_from_sensor(x, 10, True, MapCellType.OCCUPIED)
            self.mapper.update_grid_from_sensor(x, 20, True, MapCellType.OCCUPIED)

        # Create some doors
        for y in range(11, 20):
            if y == 15:  # Leave a gap for a door
                self.mapper.update_grid_from_sensor(15, y, False, MapCellType.DOOR)

        # Create an elevator
        self.mapper.update_grid_from_sensor(5, 5, False, MapCellType.ELEVATOR)

        # Create stairs
        self.mapper.update_grid_from_sensor(25, 25, False, MapCellType.STAIRS)

        # Add some random obstacles
        for _ in range(20):
            x = random.randint(0, 29)
            y = random.randint(0, 29)
            if random.random() > 0.8 and not (5 <= x <= 25 and 10 <= y <= 20):  # Avoid walls
                self.mapper.update_grid_from_sensor(x, y, True, MapCellType.OCCUPIED)

    def run_mapping_step(self) -> bool:
        """Run one step of mapping demonstration."""
        print(f"\n--- Mapping Step {self.demo_step + 1} ---")

        if self.demo_step == 0:
            # Generate initial environment
            print("Generating simulated environment...")
            self.generate_simulated_environment()
        elif self.demo_step == 1:
            # Extract topological features
            print("Extracting topological features from grid map...")
            self.mapper.extract_topological_features()
        elif self.demo_step == 2:
            # Demonstrate path planning
            print("Demonstrating path planning...")
            start = (2, 2)
            goal = (28, 28)
            grid_path = self.mapper.plan_path_grid(start, goal)
            print(f"Grid-based path from {start} to {goal}: {len(grid_path)} steps")

            # Get topological nodes if they exist
            topo_nodes = list(self.mapper.topological_map.nodes.keys())
            if len(topo_nodes) >= 2:
                topo_path = self.mapper.plan_path_topological(topo_nodes[0], topo_nodes[-1])
                print(f"Topological path from {topo_nodes[0]} to {topo_nodes[-1]}: {len(topo_path)} nodes")
        else:
            # Add more features and update maps
            x = random.randint(0, 29)
            y = random.randint(0, 29)
            is_occupied = random.random() > 0.7
            cell_type = MapCellType.FREE
            if not is_occupied and random.random() > 0.9:
                cell_type = random.choice([MapCellType.DOOR, MapCellType.ELEVATOR, MapCellType.STAIRS])
            self.mapper.update_grid_from_sensor(x, y, is_occupied, cell_type)

            # Re-extract features periodically
            if self.demo_step % 3 == 0:
                self.mapper.extract_topological_features()

        # Show map summary
        summary = self.mapper.get_map_summary()
        print(f"Grid map: {summary['grid_map']['free_cells']} free cells")
        print(f"Topological map: {summary['topological_map']['total_nodes']} nodes")

        self.demo_step += 1
        return self.demo_step < self.max_steps

    def run_demo(self):
        """Run the complete grid and topological mapping demonstration."""
        print("Grid and Topological Mapping Simulation Demo")
        print("=" * 45)
        print("Simulating how a robot creates both metric (grid) and topological")
        print("representations of its environment for navigation and spatial understanding.\n")

        print("Two mapping approaches:")
        print("- Grid mapping: Metric representation with occupancy probabilities")
        print("- Topological mapping: Waypoint-based representation with connections\n")

        print("The system demonstrates how both approaches complement each other:")
        print("- Grid maps are good for precise navigation and obstacle avoidance")
        print("- Topological maps are good for high-level path planning and reasoning\n")

        # Run the mapping simulation
        while self.run_mapping_step():
            time.sleep(0.4)  # Simulate processing time

        print(f"\nDemo completed after {self.demo_step} steps")

        # Final summary
        final_summary = self.mapper.get_map_summary()
        print(f"\nFinal Map Summary:")
        print(f"Grid Map:")
        print(f"  Dimensions: {final_summary['grid_map']['dimensions']}")
        print(f"  Free cells: {final_summary['grid_map']['free_cells']}")
        print(f"  Special features: {final_summary['grid_map']['special_features']}")

        print(f"\nTopological Map:")
        print(f"  Total nodes: {final_summary['topological_map']['total_nodes']}")
        print(f"  Node types: {final_summary['topological_map']['node_types']}")
        print(f"  Total connections: {final_summary['topological_map']['total_connections']}")


def main():
    """Main function to run the grid and topological mapping simulation."""
    demo = GridTopoMappingDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()