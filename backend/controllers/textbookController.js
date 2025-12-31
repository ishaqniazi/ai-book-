const asyncHandler = require('express-async-handler');
const TextbookContent = require('../models/TextbookContent');

// @desc    Get all textbook content
// @route   GET /api/textbook/all
// @access  Public
const getAllContent = asyncHandler(async (req, res) => {
  try {
    const content = await TextbookContent.find({}).sort({ moduleId: 1, sectionId: 1 });
    res.json(content);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// @desc    Get content by module
// @route   GET /api/textbook/module/:moduleId
// @access  Public
const getContentByModule = asyncHandler(async (req, res) => {
  try {
    const { moduleId } = req.params;
    const content = await TextbookContent.find({ moduleId }).sort({ sectionId: 1 });

    if (!content || content.length === 0) {
      return res.status(404).json({ message: 'No content found for this module' });
    }

    res.json(content);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// @desc    Get content by section
// @route   GET /api/textbook/section/:moduleId/:sectionId
// @access  Public
const getContentBySection = asyncHandler(async (req, res) => {
  try {
    const { moduleId, sectionId } = req.params;
    const content = await TextbookContent.findOne({ moduleId, sectionId });

    if (!content) {
      return res.status(404).json({ message: 'Content not found' });
    }

    res.json(content);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// @desc    Create new textbook content
// @route   POST /api/textbook/
// @access  Private
const createContent = asyncHandler(async (req, res) => {
  const {
    moduleId,
    sectionId,
    title,
    content,
    type,
    difficulty,
    prerequisites,
    estimatedTime,
    resources
  } = req.body;

  const newContent = new TextbookContent({
    moduleId,
    sectionId,
    title,
    content,
    type,
    difficulty,
    prerequisites,
    estimatedTime,
    resources
  });

  const savedContent = await newContent.save();
  res.status(201).json(savedContent);
});

// @desc    Update textbook content
// @route   PUT /api/textbook/:id
// @access  Private
const updateContent = asyncHandler(async (req, res) => {
  try {
    const content = await TextbookContent.findById(req.params.id);

    if (!content) {
      return res.status(404).json({ message: 'Content not found' });
    }

    const updatedContent = await TextbookContent.findByIdAndUpdate(
      req.params.id,
      req.body,
      { new: true, runValidators: true }
    );

    res.json(updatedContent);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// @desc    Delete textbook content
// @route   DELETE /api/textbook/:id
// @access  Private
const deleteContent = asyncHandler(async (req, res) => {
  try {
    const content = await TextbookContent.findById(req.params.id);

    if (!content) {
      return res.status(404).json({ message: 'Content not found' });
    }

    await TextbookContent.findByIdAndDelete(req.params.id);

    res.json({ message: 'Content removed' });
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

module.exports = {
  getAllContent,
  getContentByModule,
  getContentBySection,
  createContent,
  updateContent,
  deleteContent
};