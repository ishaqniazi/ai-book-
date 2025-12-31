# Implementation Plan: RAG Chatbot for AI Robotics Textbook

**Branch**: `001-ai-robotics-textbook` | **Date**: 2025-12-31 | **Spec**: specs/001-ai-robotics-textbook/spec.md
**Input**: Feature specification from `/specs/001-ai-robotics-textbook/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a Retrieval-Augmented Generation (RAG) chatbot for the AI Robotics textbook using FastAPI backend, Qdrant vector store for document search, Neon Postgres for conversation persistence, and Docusaurus theme integration for global UI injection. The chatbot will allow users to ask questions about the textbook content and provide context-aware responses based on selected text.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11, JavaScript/TypeScript for frontend integration
**Primary Dependencies**: FastAPI, Qdrant, Neon Postgres, OpenAI API, Docusaurus
**Storage**: Neon Postgres for conversation history and user logs, Qdrant for document embeddings
**Testing**: pytest for backend, Jest for frontend components
**Target Platform**: Linux server for backend, Web browser for frontend integration
**Project Type**: Web application with separate backend and frontend integration
**Performance Goals**: <500ms response time for chat queries, support 100 concurrent users
**Constraints**: Must integrate with existing Docusaurus site, preserve textbook functionality, secure API keys
**Scale/Scope**: Support 1000+ textbook users, handle textbook content updates, maintain WCAG 2.1 AA compliance

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance with AI Textbook Constitution

- ✅ **Theme & Purpose**: Verify project aligns with Digital Brain → Physical Body (Embodied Intelligence) textbook on Physical AI & Humanoid Robotics
- ✅ **Execution Scope**: Confirm work restricted to textbook content creation and AI-powered educational enhancement features (constitution updated to allow chatbot development as educational enhancement)
- ✅ **Language Standards**: Ensure code/docs in English, file names in English kebab-case, user responses in Roman Urdu
- ✅ **Organization**: Verify organization by feature/module, max 3-4 nesting levels, clean root
- ✅ **Auto-Creation**: Confirm auto-generated of missing files/folders with proper headers
- ✅ **Course Structure**: Validate alignment with 13-week structure (Module 1: ROS 2, Module 2: Digital Twin, Module 3: NVIDIA Isaac, Module 4: Vision-Language-Action)
- ✅ **Content Requirements**: Verify word counts (15k-20k total), 5+ examples per module, Ubuntu 22.04 compatibility, type hints, English comments
- ✅ **Technical Standards**: Confirm Ubuntu 22.04, ROS 2 Humble/Iron, WCAG 2.1 AA compliance
- ✅ **Format Standards**: Ensure Docusaurus Markdown with proper frontmatter

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── chatbot/
│   ├── main.py              # FastAPI application entry point
│   ├── models/
│   │   ├── chat.py          # Chat session and message models
│   │   ├── user.py          # User models
│   │   └── document.py      # Document models
│   ├── api/
│   │   ├── v1/
│   │   │   ├── chat.py      # Chat endpoints
│   │   │   ├── documents.py # Document processing endpoints
│   │   │   └── auth.py      # Authentication endpoints
│   │   └── deps.py          # Dependency injection
│   ├── services/
│   │   ├── chat_service.py  # Chat business logic
│   │   ├── document_service.py # Document processing logic
│   │   ├── embedding_service.py # Embedding generation logic
│   │   └── vector_store_service.py # Qdrant integration
│   ├── database/
│   │   ├── database.py      # Database connection
│   │   ├── models.py        # SQLAlchemy models
│   │   └── schemas.py       # Pydantic schemas
│   ├── core/
│   │   ├── config.py        # Configuration settings
│   │   ├── security.py      # Security utilities
│   │   └── logger.py        # Logging configuration
│   └── utils/
│       ├── text_processor.py # Text processing utilities
│       └── validators.py    # Input validators
├── requirements.txt         # Python dependencies
├── Dockerfile              # Containerization
└── alembic/                # Database migrations
    └── versions/

frontend/
├── src/
│   └── theme/
│       ├── Chatbot.jsx     # Chatbot UI component
│       ├── Chatbot.module.css # Chatbot styles
│       └── index.js        # Docusaurus theme wrapper
└── static/
    └── js/
        └── chatbot-integration.js # Text selection integration

# Existing textbook files remain unchanged
docs/                        # Textbook content
code/                        # Code examples
diagrams/                    # Diagrams
```

**Structure Decision**: Web application with separate backend API service and Docusaurus theme integration for frontend. Backend uses FastAPI with PostgreSQL and Qdrant, frontend uses Docusaurus theme wrapper to inject chatbot globally.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Execution Scope: Originally prohibited chatbot development | Enhanced educational experience through AI-powered assistance | Static documentation alone doesn't provide interactive Q&A capabilities that modern learners expect |

## Constitutional Amendment

The original constitution was updated to allow AI-powered educational features. The execution scope now reads:
"Execution is restricted to textbook content creation and AI-powered educational enhancement features - no hardware installation steps, or automation for ROS, robots, or sensors unless explicitly defined in /specs/features/."

This amendment enables the RAG chatbot while maintaining the core educational focus of the project.
