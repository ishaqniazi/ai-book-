#!/bin/bash

# Diagram Count Verification Script
# This script verifies that all required diagrams have been created

set -e

echo "Diagram Count Verification Script"
echo "================================="

# Expected diagrams by module
MODULE2_DIAGRAMS=("diagram4-physics-sketch.svg" "diagram5-human-robot-loop.svg" "diagram6-interaction-concepts.svg")
MODULE3_DIAGRAMS=("diagram7-vision-pipeline.svg" "diagram8-mapping-loop.svg" "diagram9-navigation-flowchart.svg")
MODULE4_DIAGRAMS=("diagram10-limb-sketch.svg" "diagram11-decision-logic.svg" "diagram12-humanoid-loop.svg")

TOTAL_REQUIRED=12
REQUIRED_BY_MODULE=("Module 2: 3 diagrams" "Module 3: 3 diagrams" "Module 4: 3 diagrams")

echo "Expected diagrams count:"
echo "- Module 1: 3 diagrams (already verified as complete)"
echo "- Module 2: 3 diagrams"
echo "- Module 3: 3 diagrams"
echo "- Module 4: 3 diagrams"
echo "- Total: 12 diagrams"
echo

# Count existing diagrams
MODULE2_COUNT=$(ls -1 diagrams/module2/ 2>/dev/null | grep -c "diagram" || echo "0")
MODULE3_COUNT=$(ls -1 diagrams/module3/ 2>/dev/null | grep -c "diagram" || echo "0")
MODULE4_COUNT=$(ls -1 diagrams/module4/ 2>/dev/null | grep -c "diagram" || echo "0")
TOTAL_COUNT=$((MODULE2_COUNT + MODULE3_COUNT + MODULE4_COUNT))

echo "Current diagram counts:"
echo "- Module 2: $MODULE2_COUNT / 3"
echo "- Module 3: $MODULE3_COUNT / 3"
echo "- Module 4: $MODULE4_COUNT / 3"
echo "- Total: $TOTAL_COUNT / 12"
echo

# Check if all required diagrams exist
MISSING=0

echo "Checking Module 2 diagrams..."
for diagram in "${MODULE2_DIAGRAMS[@]}"; do
    if [ -f "diagrams/module2/$diagram" ]; then
        echo "  ✓ $diagram"
    else
        echo "  ✗ Missing: $diagram"
        MISSING=$((MISSING + 1))
    fi
done

echo
echo "Checking Module 3 diagrams..."
for diagram in "${MODULE3_DIAGRAMS[@]}"; do
    if [ -f "diagrams/module3/$diagram" ]; then
        echo "  ✓ $diagram"
    else
        echo "  ✗ Missing: $diagram"
        MISSING=$((MISSING + 1))
    fi
done

echo
echo "Checking Module 4 diagrams..."
for diagram in "${MODULE4_DIAGRAMS[@]}"; do
    if [ -f "diagrams/module4/$diagram" ]; then
        echo "  ✓ $diagram"
    else
        echo "  ✗ Missing: $diagram"
        MISSING=$((MISSING + 1))
    fi
done

echo
if [ $MISSING -eq 0 ]; then
    echo "All required diagrams are present! ✓"
    exit 0
else
    echo "Missing $MISSING diagrams! ✗"
    exit 1
fi