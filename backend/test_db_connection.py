#!/usr/bin/env python3
"""
Test script to verify database connection and basic operations
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.models import User, Conversation, Message, Document, DocumentChunk, ChatSession, Base

# Use the Neon database URL
DATABASE_URL = "postgresql://neondb_owner:npg_wt0oFVnIXf8b@ep-aged-rice-ab3h775b-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

def test_database_connection():
    """Test the database connection"""
    try:
        # Create engine
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)

        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully")

        # Create session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()

        # Test basic operations
        print("Testing basic database operations...")

        # Create a test user
        test_user = User(
            email="test@example.com",
            username="test_user"
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print(f"✅ Created test user: {test_user.username}")

        # Create a test conversation
        test_conversation = Conversation(
            user_id=test_user.id,
            title="Test Conversation"
        )
        db.add(test_conversation)
        db.commit()
        db.refresh(test_conversation)
        print(f"✅ Created test conversation: {test_conversation.title}")

        # Create a test message
        test_message = Message(
            conversation_id=test_conversation.id,
            sender_type="user",
            content="Hello, this is a test message!"
        )
        db.add(test_message)
        db.commit()
        db.refresh(test_message)
        print(f"✅ Created test message: {test_message.content[:30]}...")

        # Test retrieval
        retrieved_user = db.query(User).filter(User.email == "test@example.com").first()
        if retrieved_user:
            print(f"✅ Retrieved user: {retrieved_user.username}")

        # Clean up - delete test records
        db.delete(test_message)
        db.delete(test_conversation)
        db.delete(test_user)
        db.commit()
        print("✅ Test records cleaned up")

        # Close session
        db.close()

        print("\n🎉 Database connection test completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False

if __name__ == "__main__":
    test_database_connection()