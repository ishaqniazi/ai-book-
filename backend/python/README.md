# AI Book Backend (Python)

This is the Python backend for the AI Robotics Textbook project, focused on AI and RAG (Retrieval-Augmented Generation) functionality.

## Overview

The Python backend provides AI-powered chatbot functionality, document processing, and RAG capabilities for the textbook content.

## Features

- FastAPI-based REST API
- RAG (Retrieval-Augmented Generation) system
- Document processing and embedding
- AI-powered chat functionality
- Integration with OpenAI API
- Qdrant vector database
- PostgreSQL database

## Tech Stack

- Python 3.11+
- FastAPI - Web framework
- SQLAlchemy - Database ORM
- Qdrant - Vector database
- OpenAI API - Language model integration
- Pydantic - Data validation

## Installation

```bash
cd backend/python
pip install -r requirements.txt
```

## Development

```bash
# Start development server
python main.py
```

## Environment Variables

Create a `.env` file in this directory with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
DATABASE_URL=your_postgresql_database_url
```

## API Endpoints

- `/v1/chat` - Chat functionality with RAG
- `/v1/documents` - Document management
- `/v1/auth` - Authentication endpoints

## Configuration

The application configuration is in the `config` directory.