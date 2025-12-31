const router = require('express').Router();
const {
  registerUser,
  loginUser,
  getUserProfile,
  updateUserProfile,
  deleteUser,
  getAllUsers
} = require('../controllers/userController');
const { protect } = require('../middleware/auth');

// @route   POST api/users/register
// @desc    Register user
// @access  Public
router.route('/register').post(registerUser);

// @route   POST api/users/login
// @desc    Login user
// @access  Public
router.route('/login').post(loginUser);

// @route   GET api/users/profile
// @desc    Get user profile
// @access  Private
router.route('/profile').get(protect, getUserProfile);

// @route   PUT api/users/profile
// @desc    Update user profile
// @access  Private
router.route('/profile').put(protect, updateUserProfile);

// @route   DELETE api/users/profile
// @desc    Delete user account
// @access  Private
router.route('/profile').delete(protect, deleteUser);

// @route   GET api/users/
// @desc    Get all users (admin only)
// @access  Private/Admin
router.route('/').get(protect, getAllUsers);

module.exports = router;