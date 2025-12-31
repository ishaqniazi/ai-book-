#!/bin/bash

# Test script for Arm Reach Logic Example
# This script tests that the example runs correctly

echo "Testing Arm Reach Logic Example..."
echo "================================="

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

echo "Python is available"

# Check if the main Python file exists
if [ ! -f "arm_reach_logic.py" ]; then
    echo "Error: arm_reach_logic.py not found"
    exit 1
fi

echo "Main Python file found"

# Run the example with a limited runtime to test functionality
echo "Running the arm reach logic (limited runtime)..."
timeout 30s python arm_reach_logic.py

# Check the exit status
if [ $? -eq 0 ]; then
    echo "Test passed: The arm reach logic ran successfully"
    exit 0
else
    echo "Test failed: The arm reach logic encountered an error"
    exit 1
fi