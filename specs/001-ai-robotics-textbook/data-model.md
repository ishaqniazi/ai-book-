# Data Model: Physical AI & Humanoid Robotics Textbook

## Key Entities

### Textbook Module
- **Fields**:
  - id: string (unique identifier, e.g., "module-1-ros2")
  - title: string (e.g., "ROS 2 Nervous System")
  - content: string (Docusaurus Markdown content)
  - wordCount: integer (target word count for module)
  - weekRange: string (e.g., "Weeks 1-5")
  - examples: array of Example IDs
  - diagrams: array of Diagram IDs
  - frontmatter: object (Docusaurus frontmatter metadata)
  - createdAt: datetime
  - updatedAt: datetime

- **Relationships**:
  - One-to-many with Code Example (one module contains multiple examples)
  - One-to-many with Diagram (one module contains multiple diagrams)

- **Validation Rules**:
  - wordCount must be within specified range (Module 1: 4k-5k, Module 2: 3.5k-4.5k, etc.)
  - title must match curriculum structure
  - content must follow Docusaurus Markdown format
  - examples must be valid and executable in Ubuntu 22.04

### Docusaurus Content
- **Fields**:
  - id: string (unique identifier)
  - moduleId: string (reference to parent module)
  - type: enum ("module", "section", "subsection")
  - content: string (Markdown/MDX content)
  - frontmatter: object (title, description, keywords, etc.)
  - accessibility: object (WCAG 2.1 AA compliance data)
  - createdAt: datetime
  - updatedAt: datetime

- **Validation Rules**:
  - Must follow Docusaurus Markdown format with proper frontmatter
  - Must meet WCAG 2.1 AA accessibility standards
  - Must include proper alt text for images

### Code Example
- **Fields**:
  - id: string (unique identifier, e.g., "example-1-module-1")
  - moduleId: string (reference to parent module)
  - title: string (descriptive title)
  - description: string (brief explanation of the example)
  - code: string (actual code content)
  - language: string (programming language)
  - environment: string ("Ubuntu 22.04")
  - dependencies: array of strings (requirements.txt or environment.yaml paths)
  - typeHints: boolean (whether type hints are included)
  - errorHandling: boolean (whether error handling is included)
  - comments: string ("English")
  - gpuRequired: boolean (tag for GPU-dependent examples)
  - testScript: string (path to test.sh)
  - createdAt: datetime
  - updatedAt: datetime

- **Relationships**:
  - Many-to-one with Textbook Module (many examples belong to one module)

- **Validation Rules**:
  - Must be executable in Ubuntu 22.04 environment
  - Must include type hints
  - Must include English comments
  - Must include basic error handling
  - Must pass test.sh validation

### Diagram
- **Fields**:
  - id: string (unique identifier, e.g., "diagram-1-module-1")
  - moduleId: string (reference to parent module)
  - title: string (descriptive title)
  - altText: string (accessibility description)
  - caption: string (descriptive caption)
  - format: enum ("SVG", "PNG")
  - path: string (relative path to diagram file)
  - accessibilityCompliant: boolean (WCAG 2.1 AA compliance)
  - createdAt: datetime
  - updatedAt: datetime

- **Relationships**:
  - Many-to-one with Textbook Module (many diagrams belong to one module)

- **Validation Rules**:
  - Must have proper alt text for accessibility
  - Must be in SVG or PNG format
  - Must meet WCAG 2.1 AA standards

### Validation Script
- **Fields**:
  - id: string (unique identifier, e.g., "script-check-wordcount")
  - name: string (script name)
  - description: string (what the script validates)
  - path: string (relative path to script file)
  - type: enum ("wordcount", "link-check", "verify")
  - language: string ("shell", "python", etc.)
  - createdAt: datetime
  - updatedAt: datetime

- **Validation Rules**:
  - Must execute without errors
  - Must provide meaningful output for validation failures

## NEW: RAG Chatbot Entities

### User
- **Fields**:
  - id: UUID (unique identifier for the user)
  - email: string (user's email address, unique)
  - username: string (user's display name)
  - created_at: datetime (account creation timestamp)
  - updated_at: datetime (last update timestamp)
  - is_active: boolean (whether the account is active)
  - preferences: JSON (user preferences for the chatbot)

- **Validation Rules**:
  - Email must be a valid email format
  - Username must be 3-50 characters
  - Email must be unique

### Conversation
- **Fields**:
  - id: UUID (unique identifier for the conversation)
  - user_id: UUID (reference to the user who owns the conversation)
  - title: string (auto-generated title for the conversation)
  - created_at: datetime (conversation creation timestamp)
  - updated_at: datetime (last interaction timestamp)
  - is_active: boolean (whether the conversation is active)

- **Validation Rules**:
  - Must have a valid user_id
  - Title must be 1-100 characters

### Message
- **Fields**:
  - id: UUID (unique identifier for the message)
  - conversation_id: UUID (reference to the parent conversation)
  - sender_type: enum ('user', 'assistant') (who sent the message)
  - content: text (the message content)
  - timestamp: datetime (when the message was sent)
  - metadata: JSON (additional message metadata, e.g., selected text context)

- **Validation Rules**:
  - Must have a valid conversation_id
  - Content must be 1-10000 characters
  - sender_type must be one of the allowed values

### Document
- **Fields**:
  - id: UUID (unique identifier for the document)
  - source_path: string (path to the original .md file)
  - title: string (title of the document)
  - content_hash: string (hash of the content for change detection)
  - created_at: datetime (when the document was first processed)
  - updated_at: datetime (when the document was last updated)
  - is_processed: boolean (whether the document embeddings are ready)

- **Validation Rules**:
  - source_path must be a valid path within docs/ directory
  - title must be 1-200 characters

### DocumentChunk
- **Fields**:
  - id: UUID (unique identifier for the chunk)
  - document_id: UUID (reference to the parent document)
  - chunk_index: integer (order of the chunk within the document)
  - content: text (the chunk content)
  - vector_id: string (ID in the vector store, Qdrant)
  - token_count: integer (number of tokens in the chunk)

- **Validation Rules**:
  - Must have a valid document_id
  - content must be 1-2000 characters
  - chunk_index must be non-negative

### ChatSession
- **Fields**:
  - id: UUID (unique identifier for the session)
  - user_id: UUID (reference to the user)
  - active_conversation_id: UUID (currently active conversation)
  - last_interaction: datetime (timestamp of last interaction)
  - session_data: JSON (additional session-specific data)

- **Validation Rules**:
  - Must have a valid user_id
  - active_conversation_id must reference an existing conversation

## Relationships for RAG Chatbot

### User ↔ Conversation
- One-to-Many: One user can have many conversations
- Foreign key: `conversations.user_id` references `users.id`
- On delete: Cascade (delete conversations when user is deleted)

### Conversation ↔ Message
- One-to-Many: One conversation can have many messages
- Foreign key: `messages.conversation_id` references `conversations.id`
- On delete: Cascade (delete messages when conversation is deleted)

### Document ↔ DocumentChunk
- One-to-Many: One document can have many chunks
- Foreign key: `document_chunks.document_id` references `documents.id`
- On delete: Cascade (delete chunks when document is deleted)

### User ↔ ChatSession
- One-to-One: One user has one active session
- Foreign key: `chat_sessions.user_id` references `users.id`
- On delete: Set null (keep session but unlink from user)

## State Transitions

### Conversation States
- `active`: Currently open for new messages
- `archived`: User has archived the conversation
- `deleted`: Marked for deletion (soft delete)

### Document Processing States
- `pending`: Document detected but not yet processed
- `processing`: Currently being chunked and embedded
- `processed`: Chunks are in vector store
- `failed`: Processing failed, needs retry