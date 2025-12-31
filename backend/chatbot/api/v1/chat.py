from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
import os
from pydantic import BaseModel

from ...database.database import get_db
from ...database.models import User, Conversation, Message
from ...services.database_service import conversation_service, message_service
from ...services.chat_service import ChatService

# Create router
router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

# Request/Response models
class StartConversationRequest(BaseModel):
    user_id: str

class StartConversationResponse(BaseModel):
    conversation_id: str
    message: str

class SendMessageRequest(BaseModel):
    message: str
    selected_text: Optional[str] = None

class SendMessageResponse(BaseModel):
    response: str
    sources: List[str]

class GetConversationResponse(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str

class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    sender_type: str
    content: str
    timestamp: str
    metadata: dict

class GetMessagesResponse(BaseModel):
    messages: List[MessageResponse]

# Initialize services
chat_service = ChatService()

@router.post("/start", response_model=StartConversationResponse)
async def start_conversation(
    request: StartConversationRequest,
    db: Session = Depends(get_db)
):
    """Start a new conversation"""
    # Get user
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create new conversation
    conversation = conversation_service.create_conversation(
        db=db,
        user_id=request.user_id,
        title="New Conversation"
    )

    return StartConversationResponse(
        conversation_id=conversation.id,
        message="New conversation started"
    )

@router.post("/{conversation_id}/message", response_model=SendMessageResponse)
async def send_message(
    conversation_id: str,
    request: SendMessageRequest,
    db: Session = Depends(get_db)
):
    """Send a message to the chatbot"""
    # Create user message
    user_message = message_service.create_message(
        db=db,
        conversation_id=conversation_id,
        sender_type="user",
        content=request.message,
        metadata={"selected_text": request.selected_text} if request.selected_text else {}
    )

    # Generate AI response using chat service
    response_data = chat_service.get_context_aware_response(
        user_message=request.message,
        selected_text=request.selected_text
    )

    # Create AI message
    ai_message = message_service.create_message(
        db=db,
        conversation_id=conversation_id,
        sender_type="assistant",
        content=response_data["response"]
    )

    return SendMessageResponse(
        response=response_data["response"],
        sources=response_data["sources"]
    )

@router.get("/{conversation_id}", response_model=GetConversationResponse)
async def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """Get conversation details"""
    conversation = conversation_service.get_conversation_by_id(
        db=db,
        conversation_id=conversation_id
    )

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return GetConversationResponse(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.created_at.isoformat(),
        updated_at=conversation.updated_at.isoformat()
    )

@router.get("/{conversation_id}/messages", response_model=GetMessagesResponse)
async def get_messages(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """Get all messages in a conversation"""
    messages = message_service.get_messages_by_conversation(
        db=db,
        conversation_id=conversation_id
    )

    return GetMessagesResponse(messages=[
        MessageResponse(
            id=msg.id,
            conversation_id=msg.conversation_id,
            sender_type=msg.sender_type,
            content=msg.content,
            timestamp=msg.timestamp.isoformat(),
            metadata=msg.metadata
        )
        for msg in messages
    ])