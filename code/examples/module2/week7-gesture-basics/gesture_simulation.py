"""
Gesture Basics Simulation Example

This script demonstrates basic gesture recognition and generation concepts
in human-robot interaction. It simulates how a robot can recognize human
gestures and generate appropriate response gestures.
"""

import math
import time
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
from enum import Enum


class GestureType(Enum):
    """Types of gestures that can be recognized or generated."""
    GREETING = "greeting"
    POINTING = "pointing"
    WAVING = "waving"
    NODDING = "nodding"
    SHAKING_HEAD = "shaking_head"
    THUMBS_UP = "thumbs_up"
    THUMBS_DOWN = "thumbs_down"
    OPEN_HAND = "open_hand"
    FIST = "fist"


class GestureComponent(Enum):
    """Components of a gesture."""
    ARM_MOVEMENT = "arm_movement"
    HAND_POSITION = "hand_position"
    HEAD_MOVEMENT = "head_movement"
    FACIAL_EXPRESSION = "facial_expression"


@dataclass
class JointPosition:
    """Represents a joint position in 3D space."""
    x: float
    y: float
    z: float
    confidence: float = 1.0  # How confident we are in this position (0.0-1.0)


@dataclass
class GestureSequence:
    """Represents a sequence of positions that form a gesture."""
    name: str
    gesture_type: GestureType
    positions: List[List[JointPosition]]  # Each element is a frame of joint positions
    duration: float  # Duration in seconds
    confidence_threshold: float = 0.7  # Minimum confidence to recognize this gesture


class GestureRecognizer:
    """Recognizes gestures from joint position data."""

    def __init__(self):
        self.known_gestures: List[GestureSequence] = self._initialize_known_gestures()
        self.confidence_threshold = 0.7

    def _initialize_known_gestures(self) -> List[GestureSequence]:
        """Initialize known gestures with example positions."""
        gestures = []

        # Simple waving gesture (arm moving back and forth)
        waving_positions = []
        for i in range(10):  # 10 frames for waving
            arm_x = math.sin(i * 0.5) * 0.2  # Oscillating motion
            arm_y = 0.5  # Arm raised to shoulder height
            arm_z = 0.0
            waving_positions.append([JointPosition(arm_x, arm_y, arm_z)])

        waving_gesture = GestureSequence(
            name="Waving",
            gesture_type=GestureType.WAVING,
            positions=waving_positions,
            duration=2.0,
            confidence_threshold=0.6
        )
        gestures.append(waving_gesture)

        # Simple pointing gesture (arm extended)
        pointing_positions = []
        for i in range(5):  # 5 frames for pointing
            arm_x = 0.3  # Arm extended forward
            arm_y = 0.2  # Arm slightly raised
            arm_z = 0.0
            pointing_positions.append([JointPosition(arm_x, arm_y, arm_z)])

        pointing_gesture = GestureSequence(
            name="Pointing",
            gesture_type=GestureType.POINTING,
            positions=pointing_positions,
            duration=1.0,
            confidence_threshold=0.7
        )
        gestures.append(pointing_gesture)

        # Simple greeting gesture (wave hello)
        greeting_positions = []
        for i in range(8):  # 8 frames for greeting
            arm_x = 0.0 if i % 2 == 0 else 0.1  # Alternating motion
            arm_y = 0.4  # Arm at chest level
            arm_z = 0.0
            greeting_positions.append([JointPosition(arm_x, arm_y, arm_z)])

        greeting_gesture = GestureSequence(
            name="Greeting Wave",
            gesture_type=GestureType.GREETING,
            positions=greeting_positions,
            duration=1.5,
            confidence_threshold=0.65
        )
        gestures.append(greeting_gesture)

        return gestures

    def recognize_gesture(self, input_sequence: List[JointPosition]) -> Tuple[Optional[GestureType], float]:
        """Recognize a gesture from input sequence of joint positions."""
        best_match = None
        best_confidence = 0.0

        for known_gesture in self.known_gestures:
            # Simple similarity calculation (in a real system, this would be more sophisticated)
            confidence = self._calculate_similarity(input_sequence, known_gesture.positions)

            if confidence > best_confidence and confidence >= known_gesture.confidence_threshold:
                best_confidence = confidence
                best_match = known_gesture.gesture_type

        return best_match, best_confidence

    def _calculate_similarity(self, input_seq: List[JointPosition], known_seq: List[List[JointPosition]]) -> float:
        """Calculate similarity between input sequence and known gesture."""
        # This is a simplified similarity calculation
        # In reality, this would use more sophisticated algorithms like DTW (Dynamic Time Warping)

        if not input_seq or not known_seq:
            return 0.0

        # Calculate average distance between corresponding points
        total_distance = 0.0
        min_len = min(len(input_seq), len(known_seq))

        for i in range(min_len):
            input_pos = input_seq[i]
            known_pos = known_seq[i][0] if known_seq[i] else input_pos  # Take first joint from frame

            # Calculate Euclidean distance
            dist = math.sqrt(
                (input_pos.x - known_pos.x)**2 +
                (input_pos.y - known_pos.y)**2 +
                (input_pos.z - known_pos.z)**2
            )

            # Convert distance to similarity (closer = higher similarity)
            similarity = max(0.0, 1.0 - dist)
            total_distance += similarity

        # Average similarity across all points
        avg_similarity = total_distance / min_len if min_len > 0 else 0.0

        # Apply confidence from input positions
        avg_confidence = sum(pos.confidence for pos in input_seq) / len(input_seq)

        # Weight the similarity by confidence
        final_similarity = avg_similarity * avg_confidence

        return final_similarity


class GestureGenerator:
    """Generates appropriate gesture responses."""

    def __init__(self):
        self.gesture_sequences: Dict[GestureType, GestureSequence] = self._initialize_gesture_sequences()

    def _initialize_gesture_sequences(self) -> Dict[GestureType, GestureSequence]:
        """Initialize gesture sequences that the robot can perform."""
        sequences = {}

        # Greeting gesture (wave back)
        greeting_positions = []
        for i in range(6):
            arm_x = 0.0 if i % 2 == 0 else 0.1
            arm_y = 0.4
            arm_z = 0.0
            greeting_positions.append([JointPosition(arm_x, arm_y, arm_z)])

        sequences[GestureType.GREETING] = GestureSequence(
            name="Robot Greeting",
            gesture_type=GestureType.GREETING,
            positions=greeting_positions,
            duration=1.2
        )

        # Acknowledgment gesture (nod)
        nodding_positions = []
        for i in range(4):
            head_y = 0.1 if i % 2 == 0 else 0.05
            head_z = 0.0
            head_x = 0.0
            nodding_positions.append([JointPosition(head_x, head_y, head_z)])

        sequences[GestureType.NODDING] = GestureSequence(
            name="Robot Nodding",
            gesture_type=GestureType.NODDING,
            positions=nodding_positions,
            duration=0.8
        )

        # Pointing gesture
        pointing_positions = []
        for i in range(3):
            arm_x = 0.3
            arm_y = 0.2
            arm_z = 0.0
            pointing_positions.append([JointPosition(arm_x, arm_y, arm_z)])

        sequences[GestureType.POINTING] = GestureSequence(
            name="Robot Pointing",
            gesture_type=GestureType.POINTING,
            positions=pointing_positions,
            duration=1.0
        )

        # Waving gesture
        waving_positions = []
        for i in range(8):
            arm_x = math.sin(i * 0.4) * 0.15
            arm_y = 0.5
            arm_z = 0.0
            waving_positions.append([JointPosition(arm_x, arm_y, arm_z)])

        sequences[GestureType.WAVING] = GestureSequence(
            name="Robot Waving",
            gesture_type=GestureType.WAVING,
            positions=waving_positions,
            duration=1.6
        )

        return sequences

    def generate_gesture(self, gesture_type: GestureType) -> Optional[GestureSequence]:
        """Generate a gesture sequence for the specified type."""
        return self.gesture_sequences.get(gesture_type)

    def get_available_gestures(self) -> List[GestureType]:
        """Get list of available gesture types."""
        return list(self.gesture_sequences.keys())

    def execute_gesture(self, gesture_sequence: GestureSequence) -> Dict:
        """Simulate executing a gesture and return execution report."""
        print(f"Executing gesture: {gesture_sequence.name}")

        # Simulate the gesture execution
        execution_log = []
        for i, frame in enumerate(gesture_sequence.positions):
            # Simulate moving to each position
            joint = frame[0] if frame else JointPosition(0, 0, 0)
            execution_log.append({
                "frame": i,
                "position": (joint.x, joint.y, joint.z),
                "timestamp": time.time()
            })
            time.sleep(0.1)  # Simulate time to move to position

        return {
            "gesture_name": gesture_sequence.name,
            "gesture_type": gesture_sequence.gesture_type.value,
            "frames_executed": len(execution_log),
            "duration": gesture_sequence.duration,
            "execution_log": execution_log
        }


class GestureInteractionDemo:
    """Main demonstration class for gesture interaction."""

    def __init__(self):
        self.gestureRecognizer = GestureRecognizer()
        self.gestureGenerator = GestureGenerator()
        self.interaction_step = 0
        self.max_steps = 5

    def simulate_human_gesture(self) -> Tuple[List[JointPosition], GestureType]:
        """Simulate a human performing a gesture."""
        # Randomly select a gesture type
        gesture_types = [GestureType.GREETING, GestureType.WAVING, GestureType.POINTING]
        selected_type = gesture_types[self.interaction_step % len(gesture_types)]

        # Create simulated joint positions for the gesture
        positions = []
        if selected_type == GestureType.GREETING:
            for i in range(5):
                arm_x = 0.0 if i % 2 == 0 else 0.08
                arm_y = 0.4
                arm_z = 0.0
                positions.append(JointPosition(arm_x, arm_y, arm_z, confidence=0.9))
        elif selected_type == GestureType.WAVING:
            for i in range(7):
                arm_x = math.sin(i * 0.6) * 0.15
                arm_y = 0.5
                arm_z = 0.0
                positions.append(JointPosition(arm_x, arm_y, arm_z, confidence=0.85))
        elif selected_type == GestureType.POINTING:
            for i in range(4):
                arm_x = 0.3
                arm_y = 0.2
                arm_z = 0.0
                positions.append(JointPosition(arm_x, arm_y, arm_z, confidence=0.95))

        return positions, selected_type

    def run_interaction_step(self) -> bool:
        """Run one step of the gesture interaction."""
        print(f"\n--- Interaction Step {self.interaction_step + 1} ---")

        # Simulate human performing a gesture
        human_positions, expected_gesture = self.simulate_human_gesture()
        print(f"Human performed gesture (expected: {expected_gesture.value}):")
        for i, pos in enumerate(human_positions[:3]):  # Show first 3 positions
            print(f"  Frame {i+1}: ({pos.x:.2f}, {pos.y:.2f}, {pos.z:.2f})")

        # Recognize the gesture
        recognized_gesture, confidence = self.gestureRecognizer.recognize_gesture(human_positions)
        print(f"\nRobot recognized: {recognized_gesture.value if recognized_gesture else 'None'} "
              f"(confidence: {confidence:.2f})")

        if recognized_gesture and confidence >= 0.6:
            # Generate an appropriate response gesture
            response_gesture = self._get_response_gesture(recognized_gesture)
            if response_gesture:
                print(f"Robot responding with: {response_gesture.value}")

                # Execute the response gesture
                gesture_seq = self.gestureGenerator.generate_gesture(response_gesture)
                if gesture_seq:
                    execution_report = self.gestureGenerator.execute_gesture(gesture_seq)
                    print(f"Gesture executed successfully: {execution_report['frames_executed']} frames")
        else:
            print("Robot did not recognize the gesture with sufficient confidence.")

        self.interaction_step += 1
        return self.interaction_step < self.max_steps

    def _get_response_gesture(self, input_gesture: GestureType) -> Optional[GestureType]:
        """Get an appropriate response gesture for the input gesture."""
        response_map = {
            GestureType.GREETING: GestureType.GREETING,
            GestureType.WAVING: GestureType.WAVING,
            GestureType.POINTING: GestureType.NODDING,
            GestureType.NODDING: GestureType.THUMBS_UP,
            GestureType.THUMBS_UP: GestureType.THUMBS_UP,
        }
        return response_map.get(input_gesture)

    def run_demo(self):
        """Run the complete gesture interaction demonstration."""
        print("Gesture Interaction Simulation Demo")
        print("=" * 35)
        print("Simulating human-robot gesture interaction with recognition and response.")
        print("The robot recognizes human gestures and responds appropriately.\n")

        print("Available gestures for recognition:")
        for gesture in self.gestureRecognizer.known_gestures:
            print(f"  - {gesture.name} ({gesture.gesture_type.value})")

        print(f"\nAvailable response gestures:")
        for gesture_type in self.gestureGenerator.get_available_gestures():
            print(f"  - {gesture_type.value}")

        # Run the interaction simulation
        while self.run_interaction_step():
            time.sleep(1.0)  # Pause between interactions

        print(f"\nDemo completed after {self.interaction_step} interaction steps")

        # Final summary
        print(f"\nSummary:")
        print(f"- Performed {self.interaction_step} gesture recognition cycles")
        print(f"- Recognized gestures: {[g.name for g in self.gestureRecognizer.known_gestures]}")


def main():
    """Main function to run the gesture interaction simulation."""
    demo = GestureInteractionDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()