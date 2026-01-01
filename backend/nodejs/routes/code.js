const router = require('express').Router();
const {
  getCodeExamples,
  runCodeExample,
  getCodeExampleById
} = require('../controllers/codeController');
const { protect } = require('../middleware/auth');

// @route   GET api/code/examples
// @desc    Get all code examples
// @access  Public
router.route('/examples').get(getCodeExamples);

// @route   GET api/code/example/:moduleId/:exampleId
// @desc    Get specific code example
// @access  Public
router.route('/example/:moduleId/:exampleId').get(getCodeExampleById);

// @route   POST api/code/run
// @desc    Run a code example (for authenticated users)
// @access  Private
router.route('/run').post(protect, runCodeExample);

module.exports = router;