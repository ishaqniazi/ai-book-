"""
Object Recognition Example

This script demonstrates basic object recognition concepts in Physical AI systems.
It simulates how a system might identify and classify objects in its environment
using feature extraction and pattern matching techniques.
"""

import time
import random
import math
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from enum import Enum


class ObjectType(Enum):
    """Types of objects that can be recognized."""
    BALL = "ball"
    BOX = "box"
    CYLINDER = "cylinder"
    TRIANGLE = "triangle"
    UNKNOWN = "unknown"


@dataclass
class ObjectFeature:
    """Represents features extracted from an object."""
    shape: str
    size: float  # Size in arbitrary units
    color: str
    texture: str
    position_x: float
    position_y: float
    confidence: float  # Recognition confidence (0.0 to 1.0)


@dataclass
class RecognizedObject:
    """Represents a recognized object with its properties."""
    object_type: ObjectType
    features: ObjectFeature
    confidence: float
    timestamp: float


class SimpleVisionSensor:
    """Simulates a simple vision sensor for object recognition."""

    def __init__(self):
        self.field_of_view = 90  # degrees
        self.resolution = (640, 480)  # pixels
        self.max_detection_distance = 10.0  # meters

    def capture_scene(self) -> List[ObjectFeature]:
        """Simulate capturing a scene with objects."""
        objects = []

        # Generate some random objects in the scene
        num_objects = random.randint(1, 5)

        for i in range(num_objects):
            # Random position within sensor range
            pos_x = random.uniform(-5.0, 5.0)
            pos_y = random.uniform(-3.0, 3.0)

            # Random object properties
            shapes = ["round", "rectangular", "cylindrical", "triangular"]
            colors = ["red", "blue", "green", "yellow", "white", "black"]
            textures = ["smooth", "rough", "bumpy", "patterned"]

            feature = ObjectFeature(
                shape=random.choice(shapes),
                size=random.uniform(0.1, 2.0),
                color=random.choice(colors),
                texture=random.choice(textures),
                position_x=pos_x,
                position_y=pos_y,
                confidence=random.uniform(0.6, 0.95)  # Base confidence
            )

            objects.append(feature)

        return objects


class ObjectRecognizer:
    """Implements basic object recognition logic."""

    def __init__(self):
        self.known_objects: Dict[str, Dict] = {
            "ball": {
                "shape": "round",
                "size_range": (0.1, 1.5),
                "common_colors": ["red", "blue", "green", "yellow"],
                "texture": "smooth"
            },
            "box": {
                "shape": "rectangular",
                "size_range": (0.2, 2.0),
                "common_colors": ["red", "blue", "white", "black"],
                "texture": "smooth"
            },
            "cylinder": {
                "shape": "cylindrical",
                "size_range": (0.3, 1.8),
                "common_colors": ["red", "blue", "green"],
                "texture": "smooth"
            },
            "triangle": {
                "shape": "triangular",
                "size_range": (0.2, 1.0),
                "common_colors": ["red", "yellow", "blue"],
                "texture": "smooth"
            }
        }

    def recognize_object(self, feature: ObjectFeature) -> RecognizedObject:
        """Recognize an object based on its features."""
        best_match = ObjectType.UNKNOWN
        best_confidence = 0.0

        # Try to match against each known object type
        for obj_type, obj_def in self.known_objects.items():
            confidence = self._calculate_match_confidence(feature, obj_def)

            if confidence > best_confidence:
                best_confidence = confidence
                best_match = ObjectType(obj_type)

        # Adjust confidence based on sensor confidence
        final_confidence = min(best_confidence * feature.confidence, 0.99)

        return RecognizedObject(
            object_type=best_match,
            features=feature,
            confidence=final_confidence,
            timestamp=time.time()
        )

    def _calculate_match_confidence(self, feature: ObjectFeature, obj_def: Dict) -> float:
        """Calculate how well a feature matches a known object definition."""
        confidence = 0.0
        total_score = 0.0
        max_score = 0.0

        # Shape matching (most important)
        if feature.shape == obj_def["shape"]:
            confidence += 0.4  # Shape match contributes 40%
        else:
            confidence += 0.05  # Partial credit for close matches

        max_score += 0.4

        # Size matching
        min_size, max_size = obj_def["size_range"]
        if min_size <= feature.size <= max_size:
            confidence += 0.2  # Size match contributes 20%
        else:
            # Partial credit for being close to range
            if feature.size < min_size:
                size_bonus = max(0, 0.1 * (1 - (min_size - feature.size) / min_size))
            else:
                size_bonus = max(0, 0.1 * (1 - (feature.size - max_size) / max_size))
            confidence += size_bonus

        max_score += 0.2

        # Color matching
        if feature.color in obj_def["common_colors"]:
            confidence += 0.2  # Color match contributes 20%
        else:
            confidence += 0.05  # Partial credit for other colors

        max_score += 0.2

        # Texture matching
        if feature.texture == obj_def["texture"]:
            confidence += 0.1  # Texture match contributes 10%
        else:
            confidence += 0.02  # Partial credit

        max_score += 0.1

        # Normalize confidence
        if max_score > 0:
            confidence = confidence / max_score
        else:
            confidence = 0.0

        return confidence

    def recognize_scene(self, features: List[ObjectFeature]) -> List[RecognizedObject]:
        """Recognize all objects in a scene."""
        recognized_objects = []

        for feature in features:
            recognized = self.recognize_object(feature)
            recognized_objects.append(recognized)

        return recognized_objects


class SceneAnalyzer:
    """Analyzes the scene and provides higher-level understanding."""

    def __init__(self):
        self.objects_history: List[List[RecognizedObject]] = []

    def analyze_scene(self, recognized_objects: List[RecognizedObject]) -> Dict:
        """Analyze the current scene and extract meaningful information."""
        analysis = {
            "total_objects": len(recognized_objects),
            "object_types": {},
            "high_confidence_objects": [],
            "spatial_distribution": {},
            "timestamp": time.time()
        }

        # Count object types
        for obj in recognized_objects:
            obj_type = obj.object_type.value
            if obj_type not in analysis["object_types"]:
                analysis["object_types"][obj_type] = 0
            analysis["object_types"][obj_type] += 1

            # Track high confidence objects
            if obj.confidence > 0.8:
                analysis["high_confidence_objects"].append(obj)

        # Analyze spatial distribution
        if recognized_objects:
            x_coords = [obj.features.position_x for obj in recognized_objects]
            y_coords = [obj.features.position_y for obj in recognized_objects]

            analysis["spatial_distribution"] = {
                "x_range": (min(x_coords), max(x_coords)),
                "y_range": (min(y_coords), max(y_coords)),
                "center_of_mass": (
                    sum(x_coords) / len(x_coords),
                    sum(y_coords) / len(y_coords)
                )
            }

        # Store in history
        self.objects_history.append(recognized_objects)

        return analysis

    def get_recognition_statistics(self) -> Dict:
        """Get statistics about recognition performance."""
        if not self.objects_history:
            return {"average_confidence": 0.0, "recognition_rate": 0.0}

        all_confidences = []
        recognized_count = 0
        total_count = 0

        for frame in self.objects_history:
            for obj in frame:
                all_confidences.append(obj.confidence)
                if obj.object_type != ObjectType.UNKNOWN:
                    recognized_count += 1
                total_count += 1

        avg_confidence = sum(all_confidences) / len(all_confidences) if all_confidences else 0.0
        recognition_rate = recognized_count / total_count if total_count > 0 else 0.0

        return {
            "average_confidence": avg_confidence,
            "recognition_rate": recognition_rate,
            "total_objects_processed": total_count,
            "recognized_objects": recognized_count
        }


class ObjectRecognitionDemo:
    """Main demonstration class for object recognition."""

    def __init__(self):
        self.sensor = SimpleVisionSensor()
        self.recognizer = ObjectRecognizer()
        self.analyzer = SceneAnalyzer()
        self.demo_steps = 0
        self.max_steps = 10  # Run for 10 steps

    def run_step(self) -> bool:
        """Run one step of the object recognition simulation."""
        print(f"\n--- Step {self.demo_steps + 1} ---")

        # Capture scene from sensor
        print("Capturing scene...")
        features = self.sensor.capture_scene()

        print(f"Detected {len(features)} objects in scene")

        # Recognize objects
        print("Recognizing objects...")
        recognized_objects = self.recognizer.recognize_scene(features)

        # Display results
        for i, obj in enumerate(recognized_objects):
            print(f"  Object {i+1}: {obj.object_type.value} "
                  f"(confidence: {obj.confidence:.2f}, "
                  f"pos: ({obj.features.position_x:.1f}, {obj.features.position_y:.1f}))")

        # Analyze scene
        analysis = self.analyzer.analyze_scene(recognized_objects)
        print(f"Scene analysis: {analysis['object_types']}")

        self.demo_steps += 1
        return self.demo_steps < self.max_steps

    def run_demo(self):
        """Run the complete object recognition demonstration."""
        print("Physical AI Object Recognition Demo")
        print("=" * 40)
        print("Simulating object recognition in a Physical AI system\n")

        start_time = time.time()

        # Run the simulation
        while self.run_step():
            time.sleep(0.5)  # Small delay to make it observable

        elapsed_time = time.time() - start_time

        # Print final statistics
        stats = self.analyzer.get_recognition_statistics()

        print(f"\nDemo completed after {elapsed_time:.2f} seconds")
        print(f"\nRecognition Statistics:")
        print(f"  Average Confidence: {stats['average_confidence']:.2f}")
        print(f"  Recognition Rate: {stats['recognition_rate']:.2f}")
        print(f"  Total Objects Processed: {stats['total_objects_processed']}")
        print(f"  Successfully Recognized: {stats['recognized_objects']}")

        print(f"\nScene Analysis Summary:")
        if self.analyzer.objects_history:
            latest_analysis = self.analyzer.objects_history[-1]
            print(f"  Most recent scene had {len(latest_analysis)} objects")


def main():
    """Main function to run the object recognition demonstration."""
    demo = ObjectRecognitionDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()