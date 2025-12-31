#!/bin/bash

# Test script for Complete System Loop Example
# This script tests that the example runs correctly

echo "Testing Complete System Loop Example..."
echo "====================================="

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

echo "Python is available"

# Check if the main Python file exists
if [ ! -f "complete_system_loop.py" ]; then
    echo "Error: complete_system_loop.py not found"
    exit 1
fi

echo "Main Python file found"

# Run the example with a limited runtime to test functionality
echo "Running the complete system loop (limited runtime)..."
timeout 50s python complete_system_loop.py

# Check the exit status
if [ $? -eq 0 ]; then
    echo "Test passed: The complete system loop ran successfully"
    exit 0
else
    echo "Test failed: The complete system loop encountered an error"
    exit 1
fi