from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Optional
import os
import uuid

class VectorStoreService:
    def __init__(self):
        # Initialize Qdrant client
        self.client = QdrantClient(
            url=os.getenv("QDRANT_URL", "https://38e2760a-931a-43db-8ebb-7f800a67815a.eu-west-2-0.aws.cloud.qdrant.io:6333"),
            api_key=os.getenv("QDRANT_API_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.W4NP-5bp7Xy-9YWIMwHd5dbcuGM_fL2Nj79HrY8vriI"),
        )

        # Collection name for document embeddings
        self.collection_name = "document_chunks"

        # Create collection if it doesn't exist
        self._create_collection()

    def _create_collection(self):
        """Create the collection if it doesn't exist"""
        try:
            collections = self.client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)

            if not collection_exists:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE)  # Assuming OpenAI embeddings
                )
                print(f"Created collection: {self.collection_name}")
            else:
                print(f"Collection {self.collection_name} already exists")
        except Exception as e:
            print(f"Error creating collection: {e}")

    def store_embeddings(self, texts: List[str], metadata: List[Dict] = None) -> List[str]:
        """
        Store embeddings in Qdrant and return the IDs
        """
        try:
            # Generate embeddings
            from .embedding_service import EmbeddingService
            embedding_service = EmbeddingService()
            embeddings = embedding_service.create_embeddings(texts)

            # Generate IDs for the points
            ids = [str(uuid.uuid4()) for _ in range(len(texts))]

            # Prepare points for insertion
            points = []
            for i, (text, embedding) in enumerate(zip(texts, embeddings)):
                payload = metadata[i] if metadata and i < len(metadata) else {}
                payload["text"] = text  # Store the original text

                points.append(models.PointStruct(
                    id=ids[i],
                    vector=embedding,
                    payload=payload
                ))

            # Insert points into collection
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            return ids
        except Exception as e:
            print(f"Error storing embeddings: {e}")
            return []

    def search_similar(self, query_text: str, limit: int = 5) -> List[Dict]:
        """
        Search for similar documents to the query text
        """
        try:
            from .embedding_service import EmbeddingService
            embedding_service = EmbeddingService()
            query_embedding = embedding_service.create_embedding(query_text)

            # Search in the collection
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit
            )

            # Format results
            results = []
            for hit in search_results:
                results.append({
                    "id": hit.id,
                    "text": hit.payload.get("text", ""),
                    "score": hit.score,
                    "metadata": {k: v for k, v in hit.payload.items() if k != "text"}
                })

            return results
        except Exception as e:
            print(f"Error searching similar documents: {e}")
            return []

    def delete_by_source_path(self, source_path: str):
        """
        Delete all embeddings associated with a specific source path
        """
        try:
            # Get all points with the specified source path
            points = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="source_path",
                            match=models.MatchValue(value=source_path)
                        )
                    ]
                ),
                limit=10000  # Adjust as needed
            )

            # Extract IDs and delete
            ids_to_delete = [point.id for point, _ in points]
            if ids_to_delete:
                self.client.delete(
                    collection_name=self.collection_name,
                    points_selector=models.PointIdsList(points=ids_to_delete)
                )
        except Exception as e:
            print(f"Error deleting embeddings by source path: {e}")

    def get_all_sources(self) -> List[str]:
        """
        Get all unique source paths in the vector store
        """
        try:
            # Get all points and extract unique source paths
            points, _ = self.client.scroll(
                collection_name=self.collection_name,
                limit=10000  # Adjust as needed
            )

            source_paths = set()
            for point, _ in points:
                source_path = point.payload.get("source_path")
                if source_path:
                    source_paths.add(source_path)

            return list(source_paths)
        except Exception as e:
            print(f"Error getting all sources: {e}")
            return []