#!/bin/bash

# Test script for Forward and Inverse Kinematics Example
# This script tests that the example runs correctly

echo "Testing Forward and Inverse Kinematics Example..."
echo "==============================================="

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

echo "Python is available"

# Check if the main Python file exists
if [ ! -f "kinematics_simulation.py" ]; then
    echo "Error: kinematics_simulation.py not found"
    exit 1
fi

echo "Main Python file found"

# Run the example with a limited runtime to test functionality
echo "Running the kinematics simulation (limited runtime)..."
timeout 35s python kinematics_simulation.py

# Check the exit status
if [ $? -eq 0 ]; then
    echo "Test passed: The kinematics simulation ran successfully"
    exit 0
else
    echo "Test failed: The kinematics simulation encountered an error"
    exit 1
fi