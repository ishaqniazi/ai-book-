# Physical AI & Humanoid Robotics Textbook

Digital Brain → Physical Body: A comprehensive guide to embodied intelligence

## Overview

This textbook provides a comprehensive guide to Physical AI and Humanoid Robotics, covering the fundamental concepts of embodied intelligence. The content is structured as a 13-week course across 4 modules, with practical examples and diagrams to illustrate key concepts.

## Project Structure

This project now includes both frontend and backend components:

- **Frontend**: Docusaurus-based documentation site (in root directory)
- **Backend**: Node.js/Express API server (in `backend/` directory)

## Features

- **Frontend**: Interactive textbook documentation with WCAG 2.1 AA accessibility
- **Backend**: User management, content API, and code example execution
- **15,000-20,000 words** of comprehensive content
- **20 conceptual code examples** demonstrating key concepts
- **12 detailed diagrams** illustrating complex concepts
- **Ubuntu 22.04 compatibility** for all examples

## Table of Contents

- **Module 1**: Foundations of Physical AI (Weeks 1-5)
  - Week 1: Foundations of Physical AI
  - Week 2: Sensing the World
  - Week 3: Motor Control & Action
  - Week 4: Perception Pipeline
  - Week 5: Digital Twin Concepts
  - Module 1 Summary

- **Module 2**: Physical Interaction & Dynamics (Weeks 6-7)
  - Week 6: Physics & Interaction Basics
  - Week 7: Human-Robot Interaction Basics
  - Module 2 Summary

- **Module 3**: Perception & Navigation (Weeks 8-10)
  - Week 8: Vision Systems (Conceptual)
  - Week 9: Mapping & Understanding Environments
  - Week 10: Navigation & Path Planning
  - Module 3 Summary

- **Module 4**: Movement & Decision Making (Weeks 11-13)
  - Week 11: Kinematics & Movement
  - Week 12: Decision-Making for Robots
  - Week 13: Full System Overview
  - Module 4 Summary

## Features

- **Frontend**: Interactive textbook documentation with WCAG 2.1 AA accessibility
- **Backend**: User management, content API, and code example execution
- **15,000-20,000 words** of comprehensive content
- **20 conceptual code examples** demonstrating key concepts
- **12 detailed diagrams** illustrating complex concepts
- **WCAG 2.1 AA accessibility compliance**
- **Ubuntu 22.04 compatibility** for all examples

## Installation & Development

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ai-textbook
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

3. Navigate to the backend directory and install backend dependencies:
   ```bash
   cd backend
   npm install
   ```

4. Create a `.env` file in the `backend/` directory with your configuration (see `backend/.env` for example)

5. Start the MongoDB database (install and start MongoDB, or use MongoDB Atlas)

6. In one terminal, start the backend server:
   ```bash
   cd backend
   npm run dev
   ```

7. In another terminal, start the frontend development server:
   ```bash
   npm start
   ```

8. Open [http://localhost:3000](http://localhost:3000) to view the textbook in your browser.

## Building for Production

To build the textbook for production:

```bash
npm run build
```

The static files will be generated in the `build` directory.

## Code Examples

The textbook includes 20 conceptual code examples across the modules:

- **Module 1 Examples**:
  - Embodiment Concepts Simulation
  - Sensor Loop Implementation
  - Balance Logic Controller
  - Object Recognition Concepts
  - Digital World Mapping

- **Module 2 Examples**:
  - Physics Scenario Simulator
  - Dialogue Manager
  - Contact/Friction Simulation
  - Attention/Intention Simulation
  - Gesture Basics Simulation

- **Module 3 Examples**:
  - Frame Analysis
  - Depth/Color/Motion Perception Pipeline
  - Pseudo Mapping
  - Grid/Topo Maps
  - Rule-Based Navigation

- **Module 4 Examples**:
  - Arm Reach Logic
  - Forward/Inverse Kinematics
  - Decision Tree Robot
  - Rule-Based Decisions
  - Complete System Loop

## Diagrams

The textbook includes 12 SVG diagrams across the modules:

- **Module 1**: Sensor → Brain → Action Flow, Perception Stages, Real World ↔ Digital World Loop
- **Module 2**: Physics Sketch, Human-Robot Loop, Interaction Concepts
- **Module 3**: Vision Pipeline, Mapping Loop, Navigation Flowchart
- **Module 4**: Limb Sketch, Decision Logic, End-to-End Humanoid Loop

## Accessibility

This textbook follows WCAG 2.1 AA accessibility guidelines:
- Proper heading hierarchy
- Sufficient color contrast
- Alternative text for images
- Semantic HTML structure
- Keyboard navigation support

## Validation Scripts

The project includes validation scripts in the `scripts` directory:
- `check-wordcount.py`: Validates word count requirements
- `link-check.sh`: Validates internal links
- `check-diagrams.sh`: Verifies diagram completeness
- `verify.sh`: Comprehensive verification script

## Deployment

The textbook has both frontend and backend components:

### Frontend Deployment
The frontend is built with Docusaurus and can be deployed to Vercel, Netlify, or any static hosting service.

For Vercel deployment:
1. Connect your GitHub repository to Vercel
2. Use the build command: `npm run build`
3. Set the output directory to: `build`

### Backend Deployment
The backend API can be deployed to services like Heroku, Railway, or any Node.js hosting platform.

For Heroku deployment:
1. Create a new app in Heroku
2. Connect to your GitHub repository
3. Set environment variables (MONGODB_URI, JWT_SECRET, etc.)
4. Deploy the `backend` directory

### Full Stack Deployment
For a complete deployment, you'll need to:
1. Deploy the frontend to a static hosting service
2. Deploy the backend to a Node.js hosting platform
3. Configure the frontend to point to your deployed backend API

## Contributing

This textbook is designed as an educational resource for Physical AI and Humanoid Robotics. Contributions and feedback are welcome.

## License

This textbook is provided as an educational resource for learning about Physical AI and Humanoid Robotics.

## About

This project demonstrates the "Digital Brain → Physical Body" paradigm of embodied intelligence, where AI systems are designed to interact with the physical world through sensing, perception, decision-making, and action.
