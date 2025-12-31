#!/bin/bash

# Test script for Physics Scenario Example
# This script tests that the example runs correctly

echo "Testing Physics Scenario Example..."
echo "====================================="

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

echo "Python is available"

# Check if the main Python file exists
if [ ! -f "physics_simulator.py" ]; then
    echo "Error: physics_simulator.py not found"
    exit 1
fi

echo "Main Python file found"

# Run the example with a limited runtime to test functionality
echo "Running the physics simulator (limited runtime)..."
timeout 15s python physics_simulator.py

# Check the exit status
if [ $? -eq 0 ]; then
    echo "Test passed: The physics simulator ran successfully"
    exit 0
else
    echo "Test failed: The physics simulator encountered an error"
    exit 1
fi