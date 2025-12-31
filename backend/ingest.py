#!/usr/bin/env python3
"""
Document ingestion script for the RAG Chatbot.
This script processes .md files from the docs/ directory,
chunks them, creates embeddings, and stores them in Qdrant.
"""

import os
import sys
from pathlib import Path
import hashlib
from typing import List, Dict
import asyncio

# Add the backend directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chatbot.database.database import get_db_session
from chatbot.database.models import Document, DocumentChunk
from chatbot.services.database_service import document_service
from chatbot.services.vector_store_service import VectorStoreService
from chatbot.services.embedding_service import EmbeddingService
from chatbot.utils.text_processor import TextProcessor


def get_all_md_files(docs_dir: str) -> List[Path]:
    """Get all .md files from the docs directory recursively."""
    docs_path = Path(docs_dir)
    md_files = list(docs_path.rglob("*.md"))
    return md_files


def calculate_content_hash(content: str) -> str:
    """Calculate SHA-256 hash of content."""
    return hashlib.sha256(content.encode()).hexdigest()


def chunk_document(content: str, chunk_size: int = 1000, overlap: int = 100) -> List[Dict]:
    """Chunk document content into smaller pieces."""
    processor = TextProcessor()
    chunks = processor.chunk_text(content, chunk_size, overlap)

    chunk_data = []
    for i, chunk in enumerate(chunks):
        chunk_data.append({
            'index': i,
            'content': chunk,
            'token_count': len(chunk.split())  # Simple token count approximation
        })

    return chunk_data


def process_document(file_path: Path, vector_store: VectorStoreService, db_session):
    """Process a single document file."""
    print(f"Processing document: {file_path}")

    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Calculate content hash
    content_hash = calculate_content_hash(content)

    # Check if document already exists and hasn't changed
    relative_path = str(file_path.relative_to(Path.cwd()))
    existing_doc = document_service.get_document_by_source_path(db_session, relative_path)

    if existing_doc:
        if existing_doc.content_hash == content_hash:
            print(f"Document {file_path} hasn't changed, skipping...")
            return
        else:
            print(f"Document {file_path} has changed, updating...")
            # Delete old embeddings from vector store
            vector_store.delete_by_source_path(relative_path)

    # Create or update document record
    if existing_doc:
        doc = existing_doc
        doc.content_hash = content_hash
        doc.updated_at = doc.__class__.updated_at.default.arg  # Use current timestamp
    else:
        doc = document_service.create_document(
            db=db_session,
            source_path=relative_path,
            title=file_path.stem,
            content_hash=content_hash
        )

    # Chunk the document
    chunk_data = chunk_document(content)

    # Create embeddings and store in vector store
    texts = [chunk['content'] for chunk in chunk_data]
    metadata = [
        {
            'source_path': relative_path,
            'document_id': doc.id,
            'chunk_index': chunk['index']
        }
        for chunk in chunk_data
    ]

    # Store embeddings in vector store
    vector_ids = vector_store.store_embeddings(texts, metadata)

    # Create document chunk records in database
    for i, chunk in enumerate(chunk_data):
        document_service.create_document_chunk(
            db=db_session,
            document_id=doc.id,
            chunk_index=chunk['index'],
            content=chunk['content'],
            token_count=chunk['token_count'],
            vector_id=vector_ids[i] if i < len(vector_ids) else None
        )

    # Update document processing status
    document_service.update_document_processed_status(db_session, doc.id, True)
    print(f"Successfully processed document: {file_path}")


def main(docs_directory: str = "docs"):
    """Main function to process all documents."""
    print("Starting document ingestion process...")

    # Initialize services
    vector_store = VectorStoreService()
    embedding_service = EmbeddingService()

    # Get all .md files
    md_files = get_all_md_files(docs_directory)
    print(f"Found {len(md_files)} .md files to process")

    # Process each file
    with get_db_session() as db_session:
        for md_file in md_files:
            try:
                process_document(md_file, vector_store, db_session)
            except Exception as e:
                print(f"Error processing {md_file}: {str(e)}")
                continue

    print("Document ingestion process completed!")


if __name__ == "__main__":
    # Allow specifying docs directory as command line argument
    docs_dir = sys.argv[1] if len(sys.argv) > 1 else "docs"
    main(docs_dir)