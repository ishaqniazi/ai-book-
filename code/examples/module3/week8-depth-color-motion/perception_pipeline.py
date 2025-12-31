"""
Perception Pipeline: Depth, Color, and Motion Analysis Example

This script demonstrates concepts of visual perception in robotics, specifically
how robots process depth, color, and motion information from their visual sensors
to understand and interact with their environment.
"""

import time
import random
import math
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
from enum import Enum


class SensorType(Enum):
    """Types of visual sensors."""
    RGB = "rgb"
    DEPTH = "depth"
    STEREO = "stereo"
    OPTICAL_FLOW = "optical_flow"


class PerceptionModality(Enum):
    """Types of perception modalities."""
    DEPTH = "depth"
    COLOR = "color"
    MOTION = "motion"


@dataclass
class DepthPoint:
    """Represents a point in 3D space with depth information."""
    x: float  # 2D image x coordinate
    y: float  # 2D image y coordinate
    z: float  # Depth (distance from camera)
    confidence: float = 1.0  # Confidence in depth measurement


@dataclass
class ColorInfo:
    """Represents color information."""
    r: float  # Red component (0.0-1.0)
    g: float  # Green component (0.0-1.0)
    b: float  # Blue component (0.0-1.0)
    hue: float  # Hue (0-360)
    saturation: float  # Saturation (0.0-1.0)
    brightness: float  # Brightness (0.0-1.0)


@dataclass
class MotionVector:
    """Represents motion information for a point."""
    dx: float  # Change in x
    dy: float  # Change in y
    magnitude: float  # Magnitude of motion
    direction: float  # Direction of motion (in radians)


@dataclass
class VisualFeature:
    """Represents a visual feature combining depth, color, and motion."""
    id: str
    position: Tuple[float, float]  # x, y in image coordinates
    depth: Optional[DepthPoint] = None
    color: Optional[ColorInfo] = None
    motion: Optional[MotionVector] = None
    feature_type: str = "unknown"
    confidence: float = 1.0


class DepthProcessor:
    """Processes depth information from sensors."""

    def __init__(self):
        self.depth_range = (0.1, 10.0)  # meters
        self.resolution = (640, 480)

    def process_depth_frame(self, raw_depth_data: List[float]) -> List[DepthPoint]:
        """Process raw depth data into depth points."""
        depth_points = []
        width, height = self.resolution

        for y in range(0, height, 10):  # Sample every 10th row for efficiency
            for x in range(0, width, 10):  # Sample every 10th column for efficiency
                idx = y * width + x
                if idx < len(raw_depth_data):
                    depth_value = raw_depth_data[idx]
                    if self.depth_range[0] <= depth_value <= self.depth_range[1]:
                        confidence = 0.9 if depth_value < 5.0 else 0.7  # Higher confidence for closer objects
                        depth_points.append(DepthPoint(
                            x=x, y=y, z=depth_value, confidence=confidence
                        ))

        return depth_points

    def segment_by_depth(self, depth_points: List[DepthPoint]) -> Dict[str, List[DepthPoint]]:
        """Segment points by depth ranges."""
        segments = {
            'near': [],
            'medium': [],
            'far': []
        }

        for point in depth_points:
            if point.z < 1.0:
                segments['near'].append(point)
            elif point.z < 3.0:
                segments['medium'].append(point)
            else:
                segments['far'].append(point)

        return segments

    def calculate_surface_normals(self, depth_points: List[DepthPoint]) -> Dict:
        """Calculate surface normals from depth points."""
        # Simplified normal calculation
        return {
            'surfaces_detected': len(depth_points) // 50,  # Estimate based on point density
            'average_surface_normal': (0.0, 0.0, 1.0)  # Simplified
        }


class ColorProcessor:
    """Processes color information from sensors."""

    def __init__(self):
        self.color_thresholds = {
            'red': (0.7, 0.3, 0.3),
            'green': (0.3, 0.7, 0.3),
            'blue': (0.3, 0.3, 0.7),
            'yellow': (0.8, 0.8, 0.2)
        }

    def process_color_frame(self, raw_color_data: List[Tuple[float, float, float]]) -> List[ColorInfo]:
        """Process raw color data into color information."""
        colors = []
        for r, g, b in raw_color_data[:100]:  # Process first 100 colors
            hue = self._rgb_to_hue(r, g, b)
            saturation = self._rgb_to_saturation(r, g, b)
            brightness = max(r, g, b)
            colors.append(ColorInfo(
                r=r, g=g, b=b, hue=hue, saturation=saturation, brightness=brightness
            ))
        return colors

    def _rgb_to_hue(self, r: float, g: float, b: float) -> float:
        """Convert RGB to hue."""
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        if max_val == min_val:
            return 0
        diff = max_val - min_val
        if max_val == r:
            h = (g - b) / diff
        elif max_val == g:
            h = 2 + (b - r) / diff
        else:
            h = 4 + (r - g) / diff
        h *= 60
        if h < 0:
            h += 360
        return h

    def _rgb_to_saturation(self, r: float, g: float, b: float) -> float:
        """Convert RGB to saturation."""
        max_val = max(r, g, b)
        if max_val == 0:
            return 0
        return (max_val - min(r, g, b)) / max_val

    def detect_color_objects(self, color_info: List[ColorInfo]) -> Dict[str, int]:
        """Detect objects based on color."""
        color_counts = {}
        for color in color_info:
            # Simple color classification
            if color.r > 0.6 and color.g < 0.4 and color.b < 0.4:
                color_counts['red'] = color_counts.get('red', 0) + 1
            elif color.r < 0.4 and color.g > 0.6 and color.b < 0.4:
                color_counts['green'] = color_counts.get('green', 0) + 1
            elif color.r < 0.4 and color.g < 0.4 and color.b > 0.6:
                color_counts['blue'] = color_counts.get('blue', 0) + 1
            else:
                color_counts['other'] = color_counts.get('other', 0) + 1

        return color_counts


class MotionProcessor:
    """Processes motion information from optical flow."""

    def __init__(self):
        self.motion_threshold = 0.5  # Minimum motion magnitude to consider

    def process_optical_flow(self, prev_frame: List[Tuple[float, float]],
                           curr_frame: List[Tuple[float, float]]) -> List[MotionVector]:
        """Process optical flow between frames."""
        motion_vectors = []
        for i in range(min(len(prev_frame), len(curr_frame))):
            prev_pos = prev_frame[i]
            curr_pos = curr_frame[i]

            dx = curr_pos[0] - prev_pos[0]
            dy = curr_pos[1] - prev_pos[1]
            magnitude = math.sqrt(dx*dx + dy*dy)
            direction = math.atan2(dy, dx)

            if magnitude > self.motion_threshold:
                motion_vectors.append(MotionVector(
                    dx=dx, dy=dy, magnitude=magnitude, direction=direction
                ))

        return motion_vectors

    def classify_motion(self, motion_vectors: List[MotionVector]) -> Dict:
        """Classify motion patterns."""
        if not motion_vectors:
            return {'type': 'static', 'description': 'No motion detected'}

        avg_magnitude = sum(m.motion.magnitude for m in motion_vectors) / len(motion_vectors)

        # Classify based on average motion
        if avg_magnitude < 2.0:
            motion_type = 'slow'
        elif avg_magnitude < 5.0:
            motion_type = 'moderate'
        else:
            motion_type = 'fast'

        # Determine dominant direction
        avg_dx = sum(m.dx for m in motion_vectors) / len(motion_vectors)
        avg_dy = sum(m.dy for m in motion_vectors) / len(motion_vectors)

        if abs(avg_dx) > abs(avg_dy):
            direction = 'horizontal' if avg_dx > 0 else 'horizontal_negative'
        else:
            direction = 'vertical' if avg_dy > 0 else 'vertical_negative'

        return {
            'type': motion_type,
            'dominant_direction': direction,
            'average_magnitude': avg_magnitude,
            'total_vectors': len(motion_vectors)
        }


class PerceptionPipeline:
    """Main perception pipeline combining depth, color, and motion processing."""

    def __init__(self):
        self.depth_processor = DepthProcessor()
        self.color_processor = ColorProcessor()
        self.motion_processor = MotionProcessor()
        self.frame_history = []

    def process_frame(self, depth_data: List[float],
                     color_data: List[Tuple[float, float, float]],
                     optical_flow: Optional[List[Tuple[float, float]]] = None) -> Dict:
        """Process a complete frame with depth, color, and motion information."""

        # Process depth
        depth_points = self.depth_processor.process_depth_frame(depth_data)
        depth_segments = self.depth_processor.segment_by_depth(depth_points)
        surface_info = self.depth_processor.calculate_surface_normals(depth_points)

        # Process color
        color_info = self.color_processor.process_color_frame(color_data)
        color_objects = self.color_processor.detect_color_objects(color_info)

        # Process motion (if optical flow data provided)
        motion_vectors = []
        motion_classification = {'type': 'static', 'description': 'No motion data'}
        if optical_flow and len(self.frame_history) > 0:
            prev_flow = self.frame_history[-1]['optical_flow'] if 'optical_flow' in self.frame_history[-1] else []
            motion_vectors = self.motion_processor.process_optical_flow(prev_flow, optical_flow)
            motion_classification = self.motion_processor.classify_motion(motion_vectors)

        # Combine all information
        perception_result = {
            'depth_analysis': {
                'total_points': len(depth_points),
                'segments': {k: len(v) for k, v in depth_segments.items()},
                'surfaces': surface_info
            },
            'color_analysis': {
                'total_colors': len(color_info),
                'detected_objects': color_objects
            },
            'motion_analysis': {
                'total_vectors': len(motion_vectors),
                'classification': motion_classification
            },
            'fused_perception': self._fuse_modalities(depth_points, color_info, motion_vectors)
        }

        # Store in history
        frame_data = {
            'depth_data': depth_data,
            'color_data': color_data,
            'optical_flow': optical_flow or [],
            'perception_result': perception_result
        }
        self.frame_history.append(frame_data)

        return perception_result

    def _fuse_modalities(self, depth_points: List[DepthPoint],
                        color_info: List[ColorInfo],
                        motion_vectors: List[MotionVector]) -> Dict:
        """Fuse information from different modalities."""
        # Simple fusion strategy - in a real system this would be more sophisticated
        fused_info = {
            'object_count_estimate': min(len(depth_points), len(color_info)) // 10,
            'dynamic_objects': len(motion_vectors) > len(depth_points) // 2,
            'environment_complexity': len(depth_points) * len(color_info) / 1000.0
        }
        return fused_info

    def get_perception_summary(self) -> Dict:
        """Get a summary of perception performance."""
        if not self.frame_history:
            return {'frames_processed': 0}

        total_depth_points = sum(len(frame['perception_result']['depth_analysis']['segments'])
                                for frame in self.frame_history)
        total_colors = sum(frame['perception_result']['color_analysis']['total_colors']
                          for frame in self.frame_history)
        total_motion = sum(frame['perception_result']['motion_analysis']['total_vectors']
                          for frame in self.frame_history)

        return {
            'frames_processed': len(self.frame_history),
            'total_depth_points_processed': total_depth_points,
            'total_colors_processed': total_colors,
            'total_motion_vectors_processed': total_motion
        }


class PerceptionDemo:
    """Main demonstration class for perception pipeline."""

    def __init__(self):
        self.pipeline = PerceptionPipeline()
        self.demo_step = 0
        self.max_steps = 6

    def generate_simulated_data(self) -> Tuple[List[float], List[Tuple[float, float, float]], List[Tuple[float, float]]]:
        """Generate simulated sensor data."""
        # Generate depth data (random values within range)
        depth_data = [random.uniform(0.5, 8.0) for _ in range(640 * 480)]

        # Generate color data (random RGB values)
        color_data = [(random.random(), random.random(), random.random()) for _ in range(100)]

        # Generate optical flow data (random 2D positions)
        optical_flow = [(random.uniform(0, 640), random.uniform(0, 480)) for _ in range(50)]

        return depth_data, color_data, optical_flow

    def run_perception_step(self) -> bool:
        """Run one step of perception processing."""
        print(f"\n--- Perception Step {self.demo_step + 1} ---")

        # Generate simulated data
        depth_data, color_data, optical_flow = self.generate_simulated_data()
        print(f"Generated simulated sensor data:")
        print(f"  - Depth points: {len(depth_data)}")
        print(f"  - Color samples: {len(color_data)}")
        print(f"  - Optical flow points: {len(optical_flow)}")

        # Process the frame
        result = self.pipeline.process_frame(depth_data, color_data, optical_flow)

        print(f"\nPerception results:")
        print(f"  Depth: {result['depth_analysis']['total_points']} points, "
              f"segments: {result['depth_analysis']['segments']}")
        print(f"  Color: {result['color_analysis']['total_colors']} colors, "
              f"objects: {result['color_analysis']['detected_objects']}")
        print(f"  Motion: {result['motion_analysis']['total_vectors']} vectors, "
              f"classification: {result['motion_analysis']['classification']['type']}")

        self.demo_step += 1
        return self.demo_step < self.max_steps

    def run_demo(self):
        """Run the complete perception pipeline demonstration."""
        print("Perception Pipeline: Depth, Color, and Motion Analysis Demo")
        print("=" * 58)
        print("Simulating how a robot processes visual information from multiple modalities:")
        print("- Depth sensing for 3D understanding")
        print("- Color processing for object recognition")
        print("- Motion analysis for dynamic scene understanding\n")

        print("The perception pipeline combines these modalities to build a comprehensive")
        print("understanding of the visual environment.\n")

        # Run the perception simulation
        while self.run_perception_step():
            time.sleep(0.5)  # Simulate processing time

        print(f"\nDemo completed after {self.demo_step} perception steps")

        # Final summary
        summary = self.pipeline.get_perception_summary()
        print(f"\nFinal Perception Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")


def main():
    """Main function to run the perception pipeline simulation."""
    demo = PerceptionDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()