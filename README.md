# AI Book Monorepo

This is a monorepo containing both frontend and backend components for the AI Robotics Textbook project.

## Project Structure

```
project-root/
├── frontend/           # Docusaurus-based textbook frontend
├── backend/
│   ├── nodejs/         # Node.js/Express API backend
│   └── python/         # Python/FastAPI RAG backend
├── docs/               # Project documentation
└── README.md
```

## Overview

This project contains an AI-powered textbook on Physical AI & Humanoid Robotics with:

- **Frontend**: A Docusaurus-based documentation site with interactive textbook content
- **Backend**: Dual backend system with Node.js API and Python RAG system

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- Python (v3.8 or higher)
- MongoDB (or MongoDB Atlas account)
- PostgreSQL (for Python backend)
- Qdrant (vector database for RAG)

### Installation

1. Clone the repository
2. Install dependencies for each component:

```bash
# Install root dependencies
npm install

# Install frontend dependencies
cd frontend && npm install && cd ..

# Install backend dependencies
cd backend/nodejs && npm install && cd ../..

# Install Python backend dependencies
cd backend/python && pip install -r requirements.txt && cd ../..
```

### Running the Application

Development:
```bash
# Run both frontend and backend concurrently
npm run dev
```

Or run components separately:

```bash
# Frontend only
cd frontend && npm start

# Node.js backend only
cd backend/nodejs && npm run dev

# Python backend only
cd backend/python && python main.py
```

## Architecture

The project is split into three main components:

### Frontend
- Built with Docusaurus
- Contains textbook content in markdown format
- Provides user interface for reading and interacting with content
- Includes AI chatbot integration

### Node.js Backend
- REST API for user management and content management
- Built with Express and MongoDB
- Handles user authentication and textbook content API

### Python Backend
- AI and RAG (Retrieval-Augmented Generation) services
- Built with FastAPI
- Integrates with OpenAI API and Qdrant vector database
- Handles document processing and AI-powered chat functionality