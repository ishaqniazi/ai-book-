#!/bin/bash

# Test script for Balance Logic Example
# This script tests that the example runs correctly

echo "Testing Balance Logic Example..."
echo "================================"

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

echo "Python is available"

# Check if the main Python file exists
if [ ! -f "balance_controller.py" ]; then
    echo "Error: balance_controller.py not found"
    exit 1
fi

echo "Main Python file found"

# Run the example with a limited runtime to test functionality
echo "Running the balance controller (limited runtime)..."
timeout 10s python balance_controller.py

# Check the exit status
if [ $? -eq 0 ]; then
    echo "Test passed: The balance controller ran successfully"
    exit 0
else
    echo "Test failed: The balance controller encountered an error"
    exit 1
fi