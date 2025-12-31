const mongoose = require('mongoose');

const { Schema } = mongoose;

// Textbook Content model
const textbookContentSchema = new Schema({
  moduleId: {
    type: String,
    required: true,
    trim: true
  },
  sectionId: {
    type: String,
    required: true,
    trim: true
  },
  title: {
    type: String,
    required: true,
    trim: true
  },
  content: {
    type: String,
    required: true
  },
  type: {
    type: String,
    enum: ['text', 'code', 'exercise', 'quiz'],
    default: 'text'
  },
  difficulty: {
    type: String,
    enum: ['beginner', 'intermediate', 'advanced'],
    default: 'beginner'
  },
  prerequisites: [String],
  estimatedTime: {
    minutes: Number
  },
  resources: [{
    name: String,
    url: String,
    type: String // 'video', 'pdf', 'code', etc.
  }],
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
});

module.exports = mongoose.model('TextbookContent', textbookContentSchema);