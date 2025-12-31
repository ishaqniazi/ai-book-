#!/bin/bash

# Test script for Pseudo Mapping Example
# This script tests that the example runs correctly

echo "Testing Pseudo Mapping Example..."
echo "================================"

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

echo "Python is available"

# Check if the main Python file exists
if [ ! -f "pseudo_mapping.py" ]; then
    echo "Error: pseudo_mapping.py not found"
    exit 1
fi

echo "Main Python file found"

# Run the example with a limited runtime to test functionality
echo "Running the pseudo mapping (limited runtime)..."
timeout 30s python pseudo_mapping.py

# Check the exit status
if [ $? -eq 0 ]; then
    echo "Test passed: The pseudo mapping ran successfully"
    exit 0
else
    echo "Test failed: The pseudo mapping encountered an error"
    exit 1
fi