#!/bin/bash

# Test script for Rule-Based Robot Example
# This script tests that the example runs correctly

echo "Testing Rule-Based Robot Example..."
echo "================================="

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

echo "Python is available"

# Check if the main Python file exists
if [ ! -f "rule_based_robot.py" ]; then
    echo "Error: rule_based_robot.py not found"
    exit 1
fi

echo "Main Python file found"

# Run the example with a limited runtime to test functionality
echo "Running the rule-based robot (limited runtime)..."
timeout 40s python rule_based_robot.py

# Check the exit status
if [ $? -eq 0 ]; then
    echo "Test passed: The rule-based robot ran successfully"
    exit 0
else
    echo "Test failed: The rule-based robot encountered an error"
    exit 1
fi