import openai
from typing import List
import os

class EmbeddingService:
    def __init__(self):
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")

    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings for a list of texts
        """
        try:
            response = self.client.embeddings.create(
                input=texts,
                model=self.model
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            print(f"Error creating embeddings: {e}")
            return []

    def create_embedding(self, text: str) -> List[float]:
        """
        Create embedding for a single text
        """
        embeddings = self.create_embeddings([text])
        return embeddings[0] if embeddings else []