#!/bin/bash

# Test script for Frame Analysis Example
# This script tests that the example runs correctly

echo "Testing Frame Analysis Example..."
echo "================================"

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

echo "Python is available"

# Check if the main Python file exists
if [ ! -f "frame_analysis.py" ]; then
    echo "Error: frame_analysis.py not found"
    exit 1
fi

echo "Main Python file found"

# Run the example with a limited runtime to test functionality
echo "Running the frame analysis (limited runtime)..."
timeout 20s python frame_analysis.py

# Check the exit status
if [ $? -eq 0 ]; then
    echo "Test passed: The frame analysis ran successfully"
    exit 0
else
    echo "Test failed: The frame analysis encountered an error"
    exit 1
fi