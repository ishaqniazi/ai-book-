"""
Attention and Intention Simulation Example

This script demonstrates concepts of attention and intention in human-robot interaction.
It simulates how a robot can focus its attention on relevant stimuli and form intentions
based on its observations and goals.
"""

import time
import random
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum


class AttentionType(Enum):
    """Types of attention mechanisms."""
    SELECTIVE = "selective"
    DIVIDED = "divided"
    SUSTAINED = "sustained"
    ALERTING = "alerting"


class IntentionType(Enum):
    """Types of intentions a robot might form."""
    GREETING = "greeting"
    ASSISTANCE = "assistance"
    EXPLORATION = "exploration"
    NAVIGATION = "navigation"
    COMMUNICATION = "communication"


@dataclass
class Stimulus:
    """Represents a sensory stimulus in the environment."""
    id: str
    intensity: float  # How strong the stimulus is (0.0-1.0)
    type: str  # What type of stimulus (visual, auditory, tactile, etc.)
    location: Tuple[float, float, float]  # x, y, z coordinates
    salience: float  # How attention-grabbing the stimulus is (0.0-1.0)
    timestamp: float  # When the stimulus was detected


@dataclass
class Intention:
    """Represents a formed intention by the robot."""
    type: IntentionType
    priority: int  # Higher number means higher priority
    target: Optional[str] = None  # Target of the intention (if applicable)
    parameters: Dict = None  # Additional parameters for the intention

    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}


class AttentionSystem:
    """Manages attention allocation in the robot."""

    def __init__(self, max_attention_spots: int = 3):
        self.max_attention_spots = max_attention_spots
        self.attention_spots: List[Stimulus] = []
        self.attention_history: List[Tuple[float, Stimulus]] = []  # (timestamp, stimulus)

    def process_stimuli(self, stimuli: List[Stimulus]) -> List[Stimulus]:
        """Process incoming stimuli and allocate attention."""
        # Sort stimuli by salience (highest first)
        sorted_stimuli = sorted(stimuli, key=lambda s: s.salience, reverse=True)

        # Allocate attention to most salient stimuli up to max_attention_spots
        self.attention_spots = sorted_stimuli[:self.max_attention_spots]

        # Record in history
        for stimulus in self.attention_spots:
            self.attention_history.append((time.time(), stimulus))

        return self.attention_spots

    def get_focused_stimuli(self) -> List[Stimulus]:
        """Get the stimuli currently in focus."""
        return self.attention_spots.copy()

    def get_attention_summary(self) -> Dict:
        """Get a summary of attention allocation."""
        return {
            "num_focused_stimuli": len(self.attention_spots),
            "total_processed": len(self.attention_history),
            "focus_distribution": {
                "visual": len([s for s in self.attention_spots if s.type == "visual"]),
                "auditory": len([s for s in self.attention_spots if s.type == "auditory"]),
                "tactile": len([s for s in self.attention_spots if s.type == "tactile"])
            }
        }


class IntentionFormationSystem:
    """Manages the formation of intentions based on attention and context."""

    def __init__(self):
        self.active_intentions: List[Intention] = []
        self.intention_history: List[Intention] = []

    def form_intentions(self, focused_stimuli: List[Stimulus], context: Dict) -> List[Intention]:
        """Form intentions based on focused stimuli and context."""
        new_intentions = []

        for stimulus in focused_stimuli:
            intention = self._form_intention_from_stimulus(stimulus, context)
            if intention:
                new_intentions.append(intention)

        # Add contextual intentions
        contextual_intentions = self._form_contextual_intentions(context)
        new_intentions.extend(contextual_intentions)

        # Sort by priority
        new_intentions.sort(key=lambda i: i.priority, reverse=True)

        # Update active intentions
        self.active_intentions = new_intentions
        self.intention_history.extend(new_intentions)

        return new_intentions

    def _form_intention_from_stimulus(self, stimulus: Stimulus, context: Dict) -> Optional[Intention]:
        """Form an intention based on a specific stimulus."""
        if stimulus.type == "visual" and stimulus.salience > 0.7:
            # High salience visual stimulus - might be a person
            return Intention(
                type=IntentionType.GREETING,
                priority=5,
                target=stimulus.id,
                parameters={"location": stimulus.location}
            )
        elif stimulus.type == "auditory" and stimulus.intensity > 0.6:
            # Audible sound - might need assistance
            return Intention(
                type=IntentionType.ASSISTANCE,
                priority=4,
                target=stimulus.id,
                parameters={"location": stimulus.location}
            )
        elif stimulus.type == "visual" and stimulus.salience > 0.4:
            # Moderate salience visual - exploration
            return Intention(
                type=IntentionType.EXPLORATION,
                priority=3,
                target=stimulus.id,
                parameters={"location": stimulus.location}
            )

        return None

    def _form_contextual_intentions(self, context: Dict) -> List[Intention]:
        """Form intentions based on broader context."""
        intentions = []

        # If there's a goal to navigate somewhere
        if context.get("navigation_goal"):
            intentions.append(Intention(
                type=IntentionType.NAVIGATION,
                priority=6,
                parameters={"destination": context["navigation_goal"]}
            ))

        # If there's a communication need
        if context.get("conversation_active"):
            intentions.append(Intention(
                type=IntentionType.COMMUNICATION,
                priority=4,
                parameters={"topic": context.get("conversation_topic", "general")}
            ))

        return intentions

    def get_active_intentions(self) -> List[Intention]:
        """Get currently active intentions."""
        return self.active_intentions.copy()

    def get_intention_summary(self) -> Dict:
        """Get a summary of intention formation."""
        return {
            "num_active_intentions": len(self.active_intentions),
            "total_formed": len(self.intention_history),
            "intention_distribution": {
                "greeting": len([i for i in self.active_intentions if i.type == IntentionType.GREETING]),
                "assistance": len([i for i in self.active_intentions if i.type == IntentionType.ASSISTANCE]),
                "exploration": len([i for i in self.active_intentions if i.type == IntentionType.EXPLORATION]),
                "navigation": len([i for i in self.active_intentions if i.type == IntentionType.NAVIGATION]),
                "communication": len([i for i in self.active_intentions if i.type == IntentionType.COMMUNICATION])
            }
        }


class AttentionIntentionDemo:
    """Main demonstration class for attention and intention systems."""

    def __init__(self):
        self.attention_system = AttentionSystem()
        self.intention_system = IntentionFormationSystem()
        self.simulation_step = 0
        self.max_steps = 10

    def generate_stimuli(self) -> List[Stimulus]:
        """Generate example stimuli for the simulation."""
        stimuli = []

        # Create some example stimuli
        for i in range(5):
            stimulus = Stimulus(
                id=f"stimulus_{i}",
                intensity=random.uniform(0.3, 1.0),
                type=random.choice(["visual", "auditory", "tactile"]),
                location=(random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10)),
                salience=random.uniform(0.2, 0.9),
                timestamp=time.time()
            )
            stimuli.append(stimulus)

        return stimuli

    def run_simulation_step(self) -> bool:
        """Run one step of the attention and intention simulation."""
        print(f"\n--- Simulation Step {self.simulation_step + 1} ---")

        # Generate stimuli for this step
        stimuli = self.generate_stimuli()
        print(f"Detected {len(stimuli)} stimuli:")
        for stim in stimuli:
            print(f"  - {stim.id}: {stim.type} (intensity: {stim.intensity:.2f}, salience: {stim.salience:.2f})")

        # Process stimuli through attention system
        focused_stimuli = self.attention_system.process_stimuli(stimuli)
        print(f"\nAttention allocated to {len(focused_stimuli)} stimuli:")
        for stim in focused_stimuli:
            print(f"  - {stim.id}: {stim.type} at {stim.location}")

        # Form intentions based on focused stimuli
        context = {
            "navigation_goal": (5.0, 0.0, 0.0) if self.simulation_step > 2 else None,
            "conversation_active": True if self.simulation_step % 3 == 0 else False
        }

        intentions = self.intention_system.form_intentions(focused_stimuli, context)
        print(f"\nFormed {len(intentions)} intentions:")
        for intent in intentions:
            print(f"  - {intent.type.value} (priority: {intent.priority})")

        # Show summaries
        attention_summary = self.attention_system.get_attention_summary()
        intention_summary = self.intention_system.get_intention_summary()

        print(f"\nAttention Summary: {attention_summary}")
        print(f"Intention Summary: {intention_summary}")

        self.simulation_step += 1
        return self.simulation_step < self.max_steps

    def run_demo(self):
        """Run the complete attention and intention demonstration."""
        print("Attention and Intention Simulation Demo")
        print("=" * 45)
        print("Simulating how a robot allocates attention and forms intentions")
        print("based on sensory input and contextual goals.\n")

        # Run the simulation
        while self.run_simulation_step():
            time.sleep(0.5)  # Small delay to simulate real-time processing

        print(f"\nDemo completed after {self.simulation_step} steps")

        # Final summary
        final_attention_summary = self.attention_system.get_attention_summary()
        final_intention_summary = self.intention_system.get_intention_summary()

        print(f"\nFinal Attention Summary: {final_attention_summary}")
        print(f"Final Intention Summary: {final_intention_summary}")

        print(f"\nTotal stimuli processed: {len(self.attention_system.attention_history)}")
        print(f"Total intentions formed: {len(self.intention_system.intention_history)}")


def main():
    """Main function to run the attention and intention simulation."""
    demo = AttentionIntentionDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()