const router = require('express').Router();
const {
  getAllContent,
  getContentByModule,
  getContentBySection,
  createContent,
  updateContent,
  deleteContent
} = require('../controllers/textbookController');
const { protect } = require('../middleware/auth');

// @route   GET api/textbook/all
// @desc    Get all textbook content
// @access  Public
router.route('/all').get(getAllContent);

// @route   GET api/textbook/module/:moduleId
// @desc    Get content by module
// @access  Public
router.route('/module/:moduleId').get(getContentByModule);

// @route   GET api/textbook/section/:moduleId/:sectionId
// @desc    Get content by section
// @access  Public
router.route('/section/:moduleId/:sectionId').get(getContentBySection);

// Protected routes for content management (instructors/admins only)
// @route   POST api/textbook/
// @desc    Create new textbook content
// @access  Private
router.route('/').post(protect, createContent);

// @route   PUT api/textbook/:id
// @desc    Update textbook content
// @access  Private
router.route('/:id').put(protect, updateContent);

// @route   DELETE api/textbook/:id
// @desc    Delete textbook content
// @access  Private
router.route('/:id').delete(protect, deleteContent);

module.exports = router;