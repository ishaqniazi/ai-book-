#!/bin/bash

# Test script for Embodiment Concepts Example
# This script tests that the example runs correctly

echo "Testing Embodiment Concepts Example..."
echo "====================================="

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

echo "Python is available"

# Check if the main Python file exists
if [ ! -f "embodiment_simulation.py" ]; then
    echo "Error: embodiment_simulation.py not found"
    exit 1
fi

echo "Main Python file found"

# Run the example with a limited number of cycles to test functionality
echo "Running the embodiment simulation (limited to 3 cycles)..."
timeout 30s python embodiment_simulation.py

# Check the exit status
if [ $? -eq 0 ]; then
    echo "Test passed: The embodiment simulation ran successfully"
    exit 0
else
    echo "Test failed: The embodiment simulation encountered an error"
    exit 1
fi