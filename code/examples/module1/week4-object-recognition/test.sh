#!/bin/bash

# Test script for Object Recognition Example
# This script tests that the example runs correctly

echo "Testing Object Recognition Example..."
echo "====================================="

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

echo "Python is available"

# Check if the main Python file exists
if [ ! -f "object_recognizer.py" ]; then
    echo "Error: object_recognizer.py not found"
    exit 1
fi

echo "Main Python file found"

# Run the example with a limited runtime to test functionality
echo "Running the object recognizer (limited runtime)..."
timeout 15s python object_recognizer.py

# Check the exit status
if [ $? -eq 0 ]; then
    echo "Test passed: The object recognizer ran successfully"
    exit 0
else
    echo "Test failed: The object recognizer encountered an error"
    exit 1
fi