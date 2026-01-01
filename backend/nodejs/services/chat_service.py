import openai
from typing import List, Dict, Optional
import os

class ChatService:
    def __init__(self):
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("CHAT_MODEL", "gpt-3.5-turbo")

        # Import services
        from .vector_store_service import VectorStoreService
        from .embedding_service import EmbeddingService
        self.vector_store = VectorStoreService()
        self.embedding_service = EmbeddingService()

    def get_context_aware_response(self, user_message: str, selected_text: Optional[str] = None) -> Dict:
        """
        Generate a context-aware response based on user message and optionally selected text
        """
        try:
            # Prepare the context
            context_texts = []

            if selected_text:
                # If there's selected text, use it as direct context
                context_texts = [selected_text]
            else:
                # Otherwise, search for relevant documents in the vector store
                search_results = self.vector_store.search_similar(user_message)
                context_texts = [result["text"] for result in search_results]

            # Build the system message with context
            if context_texts:
                context = "\n\n".join(context_texts[:3])  # Use top 3 results
                system_message = f"""You are an AI assistant for the Physical AI & Humanoid Robotics textbook.
                Use the following context from the textbook to answer the user's question:

                {context}

                If the context doesn't contain relevant information, say so."""
            else:
                system_message = "You are an AI assistant for the Physical AI & Humanoid Robotics textbook. Answer the user's question based on general knowledge about robotics and AI."

            # Create the conversation for the API call
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]

            # Call the OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )

            # Extract the response
            ai_response = response.choices[0].message.content

            # Prepare sources if context was used
            sources = []
            if context_texts:
                # In a real implementation, we'd return the actual source documents
                # For now, we'll just indicate that context was used
                sources = ["textbook_content"]  # This would be actual document paths in a full implementation

            return {
                "response": ai_response,
                "sources": sources
            }

        except Exception as e:
            print(f"Error generating response: {e}")
            return {
                "response": "Sorry, I encountered an error processing your request.",
                "sources": []
            }

    def get_basic_response(self, user_message: str) -> Dict:
        """
        Generate a basic response without specific context
        """
        return self.get_context_aware_response(user_message, None)