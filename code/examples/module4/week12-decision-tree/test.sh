#!/bin/bash

# Test script for Decision Tree Robot Example
# This script tests that the example runs correctly

echo "Testing Decision Tree Robot Example..."
echo "=================================="

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

echo "Python is available"

# Check if the main Python file exists
if [ ! -f "decision_tree_robot.py" ]; then
    echo "Error: decision_tree_robot.py not found"
    exit 1
fi

echo "Main Python file found"

# Run the example with a limited runtime to test functionality
echo "Running the decision tree robot (limited runtime)..."
timeout 40s python decision_tree_robot.py

# Check the exit status
if [ $? -eq 0 ]; then
    echo "Test passed: The decision tree robot ran successfully"
    exit 0
else
    echo "Test failed: The decision tree robot encountered an error"
    exit 1
fi