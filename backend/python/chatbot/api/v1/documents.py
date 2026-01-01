from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import os
from pydantic import BaseModel

from ...database.database import get_db
from ...database.models import Document
from ...services.database_service import document_service
from ...services.vector_store_service import VectorStoreService

# Create router
router = APIRouter(prefix="/api/v1/documents", tags=["documents"])

# Request/Response models
class DocumentResponse(BaseModel):
    id: str
    source_path: str
    title: str
    created_at: str
    updated_at: str
    is_processed: bool

class ListDocumentsResponse(BaseModel):
    documents: List[DocumentResponse]

class RefreshDocumentsResponse(BaseModel):
    message: str
    document_count: int

# Initialize services
vector_store_service = VectorStoreService()

@router.get("/", response_model=ListDocumentsResponse)
async def list_documents(db: Session = Depends(get_db)):
    """List all processed documents"""
    documents = db.query(Document).all()

    return ListDocumentsResponse(documents=[
        DocumentResponse(
            id=doc.id,
            source_path=doc.source_path,
            title=doc.title,
            created_at=doc.created_at.isoformat(),
            updated_at=doc.updated_at.isoformat(),
            is_processed=doc.is_processed
        )
        for doc in documents
    ])

@router.post("/refresh", response_model=RefreshDocumentsResponse)
async def refresh_documents(db: Session = Depends(get_db)):
    """Process all source documents and update embeddings in the vector store"""
    # This would typically involve:
    # 1. Reading all .md files from the docs/ directory
    # 2. Processing and chunking them
    # 3. Creating embeddings
    # 4. Storing in vector store

    # For now, we'll return a placeholder response
    # In a full implementation, this would call the document processing service

    # Placeholder: get all documents from the database
    documents = db.query(Document).all()
    document_count = len(documents)

    return RefreshDocumentsResponse(
        message="Document refresh process started",
        document_count=document_count
    )