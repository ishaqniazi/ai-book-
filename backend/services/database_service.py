from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
import uuid
from .models import User, Conversation, Message, Document, DocumentChunk, ChatSession
import json

class UserService:
    def create_user(self, db: Session, email: str, username: str, preferences: Optional[dict] = None) -> User:
        """Create a new user"""
        user = User(
            email=email,
            username=username,
            preferences=preferences or {}
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, db: Session, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()


class ConversationService:
    def create_conversation(self, db: Session, user_id: str, title: str) -> Conversation:
        """Create a new conversation"""
        conversation = Conversation(
            user_id=user_id,
            title=title
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation

    def get_conversation_by_id(self, db: Session, conversation_id: str) -> Optional[Conversation]:
        """Get conversation by ID"""
        return db.query(Conversation).filter(Conversation.id == conversation_id).first()

    def get_conversations_by_user(self, db: Session, user_id: str) -> List[Conversation]:
        """Get all conversations for a user"""
        return db.query(Conversation).filter(Conversation.user_id == user_id).all()

    def update_conversation_title(self, db: Session, conversation_id: str, title: str):
        """Update conversation title"""
        conversation = self.get_conversation_by_id(db, conversation_id)
        if conversation:
            conversation.title = title
            conversation.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(conversation)
        return conversation


class MessageService:
    def create_message(self, db: Session, conversation_id: str, sender_type: str, content: str, metadata: Optional[dict] = None) -> Message:
        """Create a new message"""
        message = Message(
            conversation_id=conversation_id,
            sender_type=sender_type,
            content=content,
            metadata=metadata or {}
        )
        db.add(message)
        # Update conversation timestamp
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conversation:
            conversation.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(message)
        return message

    def get_messages_by_conversation(self, db: Session, conversation_id: str) -> List[Message]:
        """Get all messages in a conversation"""
        return db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.timestamp).all()

    def get_message_by_id(self, db: Session, message_id: str) -> Optional[Message]:
        """Get message by ID"""
        return db.query(Message).filter(Message.id == message_id).first()


class DocumentService:
    def create_document(self, db: Session, source_path: str, title: str, content_hash: str) -> Document:
        """Create a new document record"""
        document = Document(
            source_path=source_path,
            title=title,
            content_hash=content_hash
        )
        db.add(document)
        db.commit()
        db.refresh(document)
        return document

    def get_document_by_source_path(self, db: Session, source_path: str) -> Optional[Document]:
        """Get document by source path"""
        return db.query(Document).filter(Document.source_path == source_path).first()

    def get_document_by_id(self, db: Session, document_id: str) -> Optional[Document]:
        """Get document by ID"""
        return db.query(Document).filter(Document.id == document_id).first()

    def update_document_processed_status(self, db: Session, document_id: str, is_processed: bool):
        """Update document processing status"""
        document = self.get_document_by_id(db, document_id)
        if document:
            document.is_processed = is_processed
            document.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(document)
        return document

    def create_document_chunk(self, db: Session, document_id: str, chunk_index: int, content: str, token_count: int, vector_id: Optional[str] = None) -> DocumentChunk:
        """Create a document chunk"""
        chunk = DocumentChunk(
            document_id=document_id,
            chunk_index=chunk_index,
            content=content,
            token_count=token_count,
            vector_id=vector_id
        )
        db.add(chunk)
        db.commit()
        db.refresh(chunk)
        return chunk

    def get_document_chunks(self, db: Session, document_id: str) -> List[DocumentChunk]:
        """Get all chunks for a document"""
        return db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).order_by(DocumentChunk.chunk_index).all()

    def get_chunk_by_vector_id(self, db: Session, vector_id: str) -> Optional[DocumentChunk]:
        """Get document chunk by vector ID"""
        return db.query(DocumentChunk).filter(DocumentChunk.vector_id == vector_id).first()


class ChatSessionService:
    def create_chat_session(self, db: Session, user_id: str, active_conversation_id: Optional[str] = None) -> ChatSession:
        """Create a new chat session"""
        session = ChatSession(
            user_id=user_id,
            active_conversation_id=active_conversation_id,
            session_data={}
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    def get_session_by_user(self, db: Session, user_id: str) -> Optional[ChatSession]:
        """Get chat session for a user"""
        return db.query(ChatSession).filter(ChatSession.user_id == user_id).first()

    def update_active_conversation(self, db: Session, user_id: str, conversation_id: str):
        """Update the active conversation for a user's session"""
        session = self.get_session_by_user(db, user_id)
        if session:
            session.active_conversation_id = conversation_id
            session.last_interaction = datetime.utcnow()
            db.commit()
            db.refresh(session)
        return session

    def update_session_data(self, db: Session, user_id: str, session_data: dict):
        """Update session data"""
        session = self.get_session_by_user(db, user_id)
        if session:
            session.session_data = session_data
            session.last_interaction = datetime.utcnow()
            db.commit()
            db.refresh(session)
        return session


# Initialize all services
user_service = UserService()
conversation_service = ConversationService()
message_service = MessageService()
document_service = DocumentService()
chat_session_service = ChatSessionService()