#!/bin/bash

# Test script for Digital World Mapping Example
# This script tests that the example runs correctly

echo "Testing Digital World Mapping Example..."
echo "========================================="

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

echo "Python is available"

# Check if the main Python file exists
if [ ! -f "digital_mapper.py" ]; then
    echo "Error: digital_mapper.py not found"
    exit 1
fi

echo "Main Python file found"

# Run the example with a limited runtime to test functionality
echo "Running the digital mapper (limited runtime)..."
timeout 20s python digital_mapper.py

# Check the exit status
if [ $? -eq 0 ]; then
    echo "Test passed: The digital mapper ran successfully"
    exit 0
else
    echo "Test failed: The digital mapper encountered an error"
    exit 1
fi