#!/bin/bash

# Test script for Contact and Friction Simulation Example
# This script tests that the example runs correctly

echo "Testing Contact and Friction Simulation Example..."
echo "==============================================="

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

echo "Python is available"

# Check if the main Python file exists
if [ ! -f "contact_friction_simulation.py" ]; then
    echo "Error: contact_friction_simulation.py not found"
    exit 1
fi

echo "Main Python file found"

# Run the example with a limited runtime to test functionality
echo "Running the contact friction simulation (limited runtime)..."
timeout 15s python contact_friction_simulation.py

# Check the exit status
if [ $? -eq 0 ]; then
    echo "Test passed: The contact friction simulation ran successfully"
    exit 0
else
    echo "Test failed: The contact friction simulation encountered an error"
    exit 1
fi