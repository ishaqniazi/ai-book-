"""
Dialogue Loop Example

This script demonstrates basic dialogue management concepts for human-robot interaction.
It simulates a simple conversation loop between a human and a robot, showing how
dialogue systems maintain context and respond appropriately.
"""

import time
import random
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum


class DialogueState(Enum):
    """Represents different states in the dialogue."""
    GREETING = "greeting"
    CONVERSATION = "conversation"
    HELP_REQUEST = "help_request"
    GOODBYE = "goodbye"
    ERROR = "error"


class IntentType(Enum):
    """Types of intents that can be recognized in user input."""
    GREETING = "greeting"
    GOODBYE = "goodbye"
    HELP = "help"
    QUESTION = "question"
    COMMAND = "command"
    CONFUSION = "confusion"


@dataclass
class DialogueContext:
    """Maintains context information for the current conversation."""
    user_name: Optional[str] = None
    conversation_topic: Optional[str] = None
    turn_count: int = 0
    last_intent: Optional[IntentType] = None
    context_memory: List[str] = None
    user_preferences: Dict[str, str] = None

    def __post_init__(self):
        if self.context_memory is None:
            self.context_memory = []
        if self.user_preferences is None:
            self.user_preferences = {}


class SimpleNLU:
    """Simple Natural Language Understanding component."""

    def __init__(self):
        self.greeting_patterns = [
            r'hello', r'hi', r'hey', r'good morning', r'good afternoon', r'good evening'
        ]
        self.goodbye_patterns = [
            r'bye', r'goodbye', r'good bye', r'see you', r'farewell', r'ciao'
        ]
        self.help_patterns = [
            r'help', r'assist', r'support', r'what can you do', r'how do i', r'help me'
        ]
        self.question_patterns = [
            r'what', r'how', r'why', r'when', r'where', r'who', r'which'
        ]

    def recognize_intent(self, text: str) -> IntentType:
        """Recognize the intent of the user's input."""
        text_lower = text.lower().strip()

        # Check for greetings
        for pattern in self.greeting_patterns:
            if re.search(pattern, text_lower):
                return IntentType.GREETING

        # Check for goodbyes
        for pattern in self.goodbye_patterns:
            if re.search(pattern, text_lower):
                return IntentType.GOODBYE

        # Check for help requests
        for pattern in self.help_patterns:
            if re.search(pattern, text_lower):
                return IntentType.HELP

        # Check for questions
        for pattern in self.question_patterns:
            if re.search(pattern, text_lower):
                return IntentType.QUESTION

        # If none of the above, it's likely a command or statement
        return IntentType.COMMAND

    def extract_entities(self, text: str) -> Dict[str, str]:
        """Extract named entities from the text."""
        entities = {}

        # Simple name extraction (assuming format like "my name is John")
        name_match = re.search(r'name is (\w+)|i am (\w+)|call me (\w+)', text.lower())
        if name_match:
            name = name_match.group(1) or name_match.group(2) or name_match.group(3)
            entities['name'] = name

        return entities


class DialogueManager:
    """Manages the dialogue flow between human and robot."""

    def __init__(self):
        self.nlu = SimpleNLU()
        self.context = DialogueContext()
        self.state = DialogueState.GREETING
        self.response_history: List[Tuple[str, str]] = []  # (user_input, robot_response)

    def process_input(self, user_input: str) -> str:
        """Process user input and generate appropriate response."""
        self.context.turn_count += 1

        # Recognize intent
        intent = self.nlu.recognize_intent(user_input)
        self.context.last_intent = intent

        # Extract entities
        entities = self.nlu.extract_entities(user_input)

        # Update context with extracted information
        if 'name' in entities and not self.context.user_name:
            self.context.user_name = entities['name']

        # Generate response based on current state and intent
        response = self._generate_response(user_input, intent, entities)

        # Update context memory
        self.context.context_memory.append(user_input)

        # Update state based on intent
        self._update_state(intent)

        # Store in history
        self.response_history.append((user_input, response))

        return response

    def _generate_response(self, user_input: str, intent: IntentType, entities: Dict) -> str:
        """Generate an appropriate response based on intent and context."""
        if intent == IntentType.GREETING:
            return self._handle_greeting()
        elif intent == IntentType.GOODBYE:
            return self._handle_goodbye()
        elif intent == IntentType.HELP:
            return self._handle_help()
        elif intent == IntentType.QUESTION:
            return self._handle_question(user_input)
        elif intent == IntentType.COMMAND:
            return self._handle_command(user_input)
        else:
            return self._handle_default(user_input)

    def _handle_greeting(self) -> str:
        """Handle greeting input."""
        if self.context.user_name:
            return f"Hello {self.context.user_name}! It's nice to meet you. How can I assist you today?"
        else:
            return "Hello! It's nice to meet you. What's your name? How can I assist you today?"

    def _handle_goodbye(self) -> str:
        """Handle goodbye input."""
        if self.context.user_name:
            return f"Goodbye {self.context.user_name}! It was nice talking with you."
        else:
            return "Goodbye! It was nice talking with you."

    def _handle_help(self) -> str:
        """Handle help requests."""
        return ("I can help with simple conversations. You can ask me questions, "
                "request information, or just chat. How can I assist you today?")

    def _handle_question(self, user_input: str) -> str:
        """Handle questions from the user."""
        # Simple question answering based on keywords
        user_lower = user_input.lower()

        if 'weather' in user_lower:
            return "I don't have access to real-time weather data, but I hope it's pleasant where you are!"
        elif 'time' in user_lower or 'day' in user_lower:
            return f"The current time is {time.strftime('%H:%M')} and today is {time.strftime('%A, %B %d')}."
        elif 'name' in user_lower:
            return "I'm a conceptual dialogue system created for educational purposes. You can call me Assistant."
        elif 'help' in user_lower:
            return "I can assist with simple conversations and questions. What would you like to know?"
        else:
            # Default question response
            return f"That's an interesting question: '{user_input}'. Can you tell me more about that?"

    def _handle_command(self, user_input: str) -> str:
        """Handle command or statement input."""
        # Look for specific commands
        user_lower = user_input.lower()

        if 'thank' in user_lower:
            return "You're welcome! Is there anything else I can help with?"
        elif 'how are you' in user_lower or 'how do you do' in user_lower:
            return "I'm functioning well, thank you for asking! How can I assist you today?"
        else:
            # Default response for statements
            return f"I see. Tell me more about '{user_input.split()[0] if user_input.split() else 'that'}'."

    def _handle_default(self, user_input: str) -> str:
        """Handle input that doesn't match specific intents."""
        return f"I'm not sure I understand. Could you rephrase '{user_input[:30]}{'...' if len(user_input) > 30 else ''}'?"

    def _update_state(self, intent: IntentType):
        """Update the dialogue state based on the intent."""
        if intent == IntentType.GOODBYE:
            self.state = DialogueState.GOODBYE
        elif intent == IntentType.HELP:
            self.state = DialogueState.HELP_REQUEST
        else:
            self.state = DialogueState.CONVERSATION

    def get_context_summary(self) -> str:
        """Get a summary of the current dialogue context."""
        summary = f"Turns: {self.context.turn_count}"
        if self.context.user_name:
            summary += f", User: {self.context.user_name}"
        if self.context.last_intent:
            summary += f", Last intent: {self.context.last_intent.value}"
        return summary


class DialogueDemo:
    """Main demonstration class for the dialogue system."""

    def __init__(self):
        self.dialogue_manager = DialogueManager()
        self.demo_steps = 0
        self.max_turns = 10  # Maximum conversation turns
        self.simulated_conversation = [
            "Hello there!",
            "My name is Alex",
            "How are you today?",
            "What can you help me with?",
            "Tell me about robotics",
            "Thanks for the information",
            "What time is it?",
            "I need to go now",
            "Goodbye",
            "See you later"
        ]

    def run_conversation_step(self, user_input: str = None) -> bool:
        """Run one step of the conversation."""
        if user_input is None:
            if self.demo_steps < len(self.simulated_conversation):
                user_input = self.simulated_conversation[self.demo_steps]
            else:
                return False  # End of demo

        print(f"\nUser: {user_input}")

        # Process the input and get response
        response = self.dialogue_manager.process_input(user_input)
        print(f"Robot: {response}")

        # Show context summary
        context_summary = self.dialogue_manager.get_context_summary()
        print(f"[Context: {context_summary}]")

        # Check if conversation should end
        if self.dialogue_manager.state == DialogueState.GOODBYE:
            print("\nConversation ended by user request.")
            return False

        self.demo_steps += 1
        return self.demo_steps < self.max_turns

    def run_demo(self):
        """Run the complete dialogue demonstration."""
        print("Physical AI Dialogue Loop Demo")
        print("=" * 40)
        print("Simulating human-robot conversation with context management\n")

        print("Initial state:")
        print(f"Context: {self.dialogue_manager.get_context_summary()}")
        print()

        start_time = time.time()

        # Run the conversation
        while self.run_conversation_step():
            time.sleep(0.5)  # Small delay to simulate real conversation

        elapsed_time = time.time() - start_time

        # Print final summary
        print(f"\nDemo completed after {elapsed_time:.2f} seconds")
        print(f"Total conversation turns: {self.dialogue_manager.context.turn_count}")
        print(f"Final context: {self.dialogue_manager.get_context_summary()}")

        # Show conversation history
        print(f"\nConversation history:")
        for i, (user, robot) in enumerate(self.dialogue_manager.response_history, 1):
            print(f"  {i}. User: {user}")
            print(f"     Robot: {robot}")


def main():
    """Main function to run the dialogue demonstration."""
    demo = DialogueDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()