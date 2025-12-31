#!/bin/bash

# Test script for Attention and Intention Simulation Example
# This script tests that the example runs correctly

echo "Testing Attention and Intention Simulation Example..."
echo "=================================================="

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

echo "Python is available"

# Check if the main Python file exists
if [ ! -f "attention_intention_simulation.py" ]; then
    echo "Error: attention_intention_simulation.py not found"
    exit 1
fi

echo "Main Python file found"

# Run the example with a limited runtime to test functionality
echo "Running the attention intention simulation (limited runtime)..."
timeout 20s python attention_intention_simulation.py

# Check the exit status
if [ $? -eq 0 ]; then
    echo "Test passed: The attention intention simulation ran successfully"
    exit 0
else
    echo "Test failed: The attention intention simulation encountered an error"
    exit 1
fi