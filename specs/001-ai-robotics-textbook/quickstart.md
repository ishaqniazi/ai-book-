# Quickstart Guide: Physical AI & Humanoid Robotics Textbook

## Prerequisites

- Node.js 18+ installed
- Docusaurus installed globally (`npm install -g @docusaurus/init`)
- Git installed
- Ubuntu 22.04 (for running code examples)

## Setup Instructions

### 1. Clone and Initialize the Repository

```bash
# Clone your repository (after creating it manually)
git clone <your-repo-url>
cd <repo-name>

# Install dependencies
npm install
```

### 2. Local Development

```bash
# Start the development server
npm start

# This will start a local server at http://localhost:3000
```

### 3. Running Code Examples

Each module contains 5 code examples that can be run in an Ubuntu 22.04 environment:

```bash
# Navigate to a specific example
cd code/module-1/example-1

# Install dependencies (if any)
pip install -r requirements.txt  # or conda env create -f environment.yaml

# Run the example
python main.py
```

### 4. Building the Textbook

```bash
# Build the static site
npm run build

# The output will be in the build/ directory
```

### 5. Validation Scripts

Run these scripts before submitting or deploying:

```bash
# Check word count compliance
python scripts/check-wordcount.py

# Check for broken links
bash scripts/link-check.sh

# Run comprehensive verification
bash scripts/verify.sh
```

## Textbook Structure

```
docs/                    # Textbook modules content (Docusaurus markdown)
├── module-1-ros2/       # Module 1: ROS 2 Nervous System (Weeks 1-5)
├── module-2-digital-twin/ # Module 2: Digital Twin (Weeks 6-7)
├── module-3-nvidia-isaac/ # Module 3: NVIDIA Isaac AI Brain (Weeks 8-10)
└── module-4-vision-language-action/ # Module 4: Vision-Language-Action (Weeks 11-13)
diagrams/                # 12 diagrams (3 per module)
code/                    # 20 runnable examples (5 per module)
examples/                # Example metadata (meta.yaml)
scripts/                 # CI scripts
static/                  # Docusaurus static assets
```

## Module Breakdown

### Module 1: ROS 2 Nervous System (Weeks 1-5)
- Target: 4,000-5,000 words
- 5 code examples with Ubuntu 22.04 compatibility
- 3 diagrams for visual explanation

### Module 2: Digital Twin (Weeks 6-7)
- Target: 3,500-4,500 words
- 5 code examples with Ubuntu 22.04 compatibility
- 3 diagrams for visual explanation

### Module 3: NVIDIA Isaac AI Brain (Weeks 8-10)
- Target: 4,000-5,000 words
- 5 code examples with Ubuntu 22.04 compatibility
- 3 diagrams for visual explanation

### Module 4: Vision-Language-Action (Weeks 11-13)
- Target: 3,500-4,500 words
- 5 code examples with Ubuntu 22.04 compatibility
- 3 diagrams for visual explanation

## Example Metadata Format

Examples include metadata in `examples/meta.yaml`:

```yaml
- id: example-1-module-1
  title: "Basic ROS 2 Publisher/Subscriber"
  description: "Simple publisher and subscriber nodes"
  language: "python"
  requires_gpu: false
  dependencies: ["rclpy", "std_msgs"]
  ubuntu_compatible: true
```

## Diagram Metadata Format

Diagrams include metadata in `diagrams/meta.yaml`:

```yaml
- id: diagram-1-module-1
  title: "ROS 2 Architecture Overview"
  alt_text: "Diagram showing ROS 2 architecture with nodes, topics, and services"
  caption: "ROS 2 communication architecture with publisher-subscriber pattern"
  format: "SVG"
  accessibility_compliant: true
```

## Deployment

The textbook is deployed to Vercel:

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy to Vercel
vercel --prod
```

## Accessibility Compliance

All content meets WCAG 2.1 AA standards:
- Proper heading hierarchy
- Alt text for all images
- Sufficient color contrast
- Keyboard navigation support
- Screen reader compatibility

## NEW: RAG Chatbot Integration

### Prerequisites for Chatbot
- Python 3.9+ installed
- Access to OpenAI API (or alternative LLM provider)
- Neon Postgres account for database storage
- Qdrant Cloud account for vector storage

### Setup Instructions for Chatbot

#### 1. Backend Setup
```bash
# Navigate to the backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and database URLs
```

#### 2. Database Setup
```bash
# Run database migrations
alembic upgrade head
```

#### 3. Document Processing
```bash
# Process textbook documents to populate vector store
python -m chatbot.scripts.process_documents
```

#### 4. Start the Backend
```bash
# Start the FastAPI server
uvicorn chatbot.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Integration
The chatbot UI is automatically integrated into the Docusaurus site through the theme wrapper. No additional setup is required.

### API Endpoints
- Chat: `POST /api/v1/chat/{conversation_id}/message`
- Documents: `GET /api/v1/documents/`
- Authentication: `POST /api/v1/auth/login`

### Text Selection Feature
The chatbot supports asking questions about selected text on the page. Users can select text and click the chatbot icon to ask context-specific questions.