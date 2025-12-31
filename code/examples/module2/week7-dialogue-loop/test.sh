#!/bin/bash

# Test script for Dialogue Loop Example
# This script tests that the example runs correctly

echo "Testing Dialogue Loop Example..."
echo "================================="

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

echo "Python is available"

# Check if the main Python file exists
if [ ! -f "dialogue_manager.py" ]; then
    echo "Error: dialogue_manager.py not found"
    exit 1
fi

echo "Main Python file found"

# Run the example with a limited runtime to test functionality
echo "Running the dialogue manager (limited runtime)..."
timeout 20s python dialogue_manager.py

# Check the exit status
if [ $? -eq 0 ]; then
    echo "Test passed: The dialogue manager ran successfully"
    exit 0
else
    echo "Test failed: The dialogue manager encountered an error"
    exit 1
fi