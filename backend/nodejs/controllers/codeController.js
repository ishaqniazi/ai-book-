const asyncHandler = require('express-async-handler');
const { PythonShell } = require('python-shell');
const path = require('path');

// @desc    Get all code examples
// @route   GET /api/code/examples
// @access  Public
const getCodeExamples = asyncHandler(async (req, res) => {
  try {
    // Return a structured list of available code examples
    const codePath = path.join(__dirname, '../../code/examples');

    // In a real implementation, you would scan the directory structure
    // For now, return a sample structure
    const examples = {
      module1: {
        name: 'Foundations of Physical AI',
        examples: ['basic_robot_control.py', 'motor_control.py']
      },
      module2: {
        name: 'Human-Robot Interaction',
        examples: ['gesture_simulation.py', 'interaction_basics.py']
      },
      module3: {
        name: 'Vision and Navigation',
        examples: ['grid_topo_mapping.py', 'pseudo_mapping.py', 'vision_systems.py']
      },
      module4: {
        name: 'Decision Making',
        examples: ['decision_tree_robot.py', 'full_system.py']
      }
    };

    res.json(examples);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// @desc    Get specific code example
// @route   GET /api/code/example/:moduleId/:exampleId
// @access  Public
const getCodeExampleById = asyncHandler(async (req, res) => {
  try {
    const { moduleId, exampleId } = req.params;

    // In a real implementation, you would read the actual file content
    // For now, return a sample response
    const examplePath = path.join(__dirname, `../../code/examples/${moduleId}/${exampleId}`);

    // Note: In a real implementation, you'd want to validate the path to prevent directory traversal
    res.json({
      moduleId,
      exampleId,
      path: examplePath,
      content: `# This would be the content of ${exampleId} from ${moduleId}`
    });
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// @desc    Run a code example
// @route   POST /api/code/run
// @access  Private
const runCodeExample = asyncHandler(async (req, res) => {
  try {
    const { moduleId, exampleId, args = [] } = req.body;

    // Validate inputs
    if (!moduleId || !exampleId) {
      return res.status(400).json({ message: 'Module ID and Example ID are required' });
    }

    // Construct the path to the Python file
    const pythonFilePath = path.join(__dirname, `../../code/examples/${moduleId}/${exampleId}`);

    // Options for PythonShell
    const options = {
      mode: 'text',
      pythonPath: 'python', // or 'python3' depending on your system
      pythonOptions: ['-u'],
      args: args
    };

    // Run the Python script
    PythonShell.run(pythonFilePath, options, (err, results) => {
      if (err) {
        console.error('Error running Python script:', err);
        return res.status(500).json({
          message: 'Error running code example',
          error: err.message
        });
      }

      res.json({
        success: true,
        output: results,
        moduleId,
        exampleId
      });
    });

  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

module.exports = {
  getCodeExamples,
  runCodeExample,
  getCodeExampleById
};