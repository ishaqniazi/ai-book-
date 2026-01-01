# AI Book Backend (Node.js)

This is the Node.js backend for the AI Robotics Textbook project.

## Overview

The backend provides REST APIs for textbook content management, user authentication, and integration with various services.

## Features

- RESTful API endpoints
- User authentication and management
- Textbook content API
- Integration with Python services
- MongoDB database integration

## Tech Stack

- Node.js
- Express.js - Web framework
- Mongoose - MongoDB ODM
- JSON Web Tokens (JWT) - Authentication
- Bcrypt - Password hashing
- Python-Shell - Integration with Python services

## Installation

```bash
cd backend/nodejs
npm install
```

## Development

```bash
# Start development server with auto-reload
npm run dev

# Start production server
npm run start
```

## Environment Variables

Create a `.env` file in the root of the backend directory with the following variables:

```env
PORT=3000
MONGODB_URI=your_mongodb_connection_string
JWT_SECRET=your_jwt_secret
```

## API Endpoints

- `/api/textbook` - Textbook content management
- `/api/users` - User authentication and management
- `/api/code` - Python code examples execution

## Database

The application uses MongoDB for data storage. Models are defined in the `models` directory.