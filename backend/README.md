# AI Robotics Textbook Backend

This is the backend API for the AI Robotics Textbook project, built with Node.js and Express.

## Features

- User authentication and authorization
- Textbook content management
- Code example execution
- Progress tracking for students

## Prerequisites

- Node.js (v16 or higher)
- MongoDB (or MongoDB Atlas account)
- Python (for running code examples)

## Installation

1. Clone the repository
2. Navigate to the backend directory: `cd backend`
3. Install dependencies: `npm install`
4. Create a `.env` file based on `.env.example`
5. Start MongoDB server
6. Run the server: `npm run dev`

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```bash
PORT=5000
NODE_ENV=development
MONGODB_URI=mongodb://localhost:27017/ai-robotics-textbook
JWT_SECRET=your-super-secret-jwt-key-change-in-production
PYTHON_PATH=python
FRONTEND_URL=http://localhost:3000
```

## API Endpoints

### Textbook Content
- `GET /api/textbook/all` - Get all textbook content
- `GET /api/textbook/module/:moduleId` - Get content by module
- `POST /api/textbook/` - Create new content (auth required)
- `PUT /api/textbook/:id` - Update content (auth required)
- `DELETE /api/textbook/:id` - Delete content (auth required)

### Users
- `POST /api/users/register` - Register a new user
- `POST /api/users/login` - Login user
- `GET /api/users/profile` - Get user profile (auth required)
- `PUT /api/users/profile` - Update user profile (auth required)

### Code Examples
- `GET /api/code/examples` - Get all code examples
- `POST /api/code/run` - Run a code example (auth required)

## Running the Application

Development:
```bash
npm run dev
```

Production:
```bash
npm start
```

## Project Structure

```
backend/
├── controllers/     # Request handlers
├── models/          # Database models
├── routes/          # API routes
├── middleware/      # Authentication and other middleware
├── utils/           # Utility functions
├── config/          # Configuration files
├── server.js        # Main server file
└── package.json     # Dependencies and scripts
```