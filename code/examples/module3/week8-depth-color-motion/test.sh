#!/bin/bash

# Test script for Perception Pipeline Example
# This script tests that the example runs correctly

echo "Testing Perception Pipeline Example..."
echo "====================================="

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

echo "Python is available"

# Check if the main Python file exists
if [ ! -f "perception_pipeline.py" ]; then
    echo "Error: perception_pipeline.py not found"
    exit 1
fi

echo "Main Python file found"

# Run the example with a limited runtime to test functionality
echo "Running the perception pipeline (limited runtime)..."
timeout 25s python perception_pipeline.py

# Check the exit status
if [ $? -eq 0 ]; then
    echo "Test passed: The perception pipeline ran successfully"
    exit 0
else
    echo "Test failed: The perception pipeline encountered an error"
    exit 1
fi