from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Import the API routers
from chatbot.api.v1.chat import router as chat_router
from chatbot.api.v1.documents import router as documents_router
from chatbot.api.v1.auth import router as auth_router
from chatbot.database.database import init_db

# Create FastAPI app
app = FastAPI(
    title="RAG Chatbot API for AI Robotics Textbook",
    description="API for the Retrieval-Augmented Generation chatbot that allows users to ask questions about the AI Robotics textbook content",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Event handlers
@app.on_event("startup")
def on_startup():
    """Initialize database on startup"""
    init_db()
    print("Database initialized successfully")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "chatbot-api"}

# Include API routers
app.include_router(chat_router)
app.include_router(documents_router)
app.include_router(auth_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)