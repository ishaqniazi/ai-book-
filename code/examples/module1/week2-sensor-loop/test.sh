#!/bin/bash

# Test script for Sensor Loop Example
# This script tests that the example runs correctly

echo "Testing Sensor Loop Example..."
echo "==============================="

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

echo "Python is available"

# Check if the main Python file exists
if [ ! -f "sensor_loop.py" ]; then
    echo "Error: sensor_loop.py not found"
    exit 1
fi

echo "Main Python file found"

# Run the example with a limited runtime to test functionality
echo "Running the sensor loop (limited runtime)..."
timeout 15s python sensor_loop.py

# Check the exit status
if [ $? -eq 0 ]; then
    echo "Test passed: The sensor loop ran successfully"
    exit 0
else
    echo "Test failed: The sensor loop encountered an error"
    exit 1
fi