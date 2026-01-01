const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
const path = require('path');

require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files from the 'code' directory to allow access to Python examples
app.use('/api/code', express.static(path.join(__dirname, '../code')));

// Database connection
const uri = process.env.MONGODB_URI || 'mongodb://localhost:27017/ai-robotics-textbook';
mongoose.connect(uri, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

const connection = mongoose.connection;
connection.once('open', () => {
  console.log('MongoDB database connection established successfully');
});

// API Routes
const textbookRoutes = require('./routes/textbook');
const userRoutes = require('./routes/user');
const codeRoutes = require('./routes/code');

app.use('/api/textbook', textbookRoutes);
app.use('/api/users', userRoutes);
app.use('/api/code', codeRoutes);

// Serve frontend build in production
if (process.env.NODE_ENV === 'production') {
  app.use(express.static(path.join(__dirname, '../build')));

  app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../build', 'index.html'));
  });
}

app.listen(PORT, () => {
  console.log(`Server is running on port: ${PORT}`);
});