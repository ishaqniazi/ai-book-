#!/bin/bash

# Comprehensive Verification Script
# This script runs all validation checks to ensure the textbook meets requirements

set -e

echo "Comprehensive Textbook Verification"
echo "==================================="

# Check if required directories exist
echo "Checking directory structure..."
if [ ! -d "docs" ]; then
    echo "✗ docs directory not found"
    exit 1
else
    echo "✓ docs directory exists"
fi

if [ ! -d "diagrams" ]; then
    echo "✗ diagrams directory not found"
    exit 1
else
    echo "✓ diagrams directory exists"
fi

if [ ! -d "code" ]; then
    echo "✗ code directory not found"
    exit 1
else
    echo "✓ code directory exists"
fi

if [ ! -d "scripts" ]; then
    echo "✗ scripts directory not found"
    exit 1
else
    echo "✓ scripts directory exists"
fi

echo

# Count content files
MODULE1_COUNT=$(find docs/module1 -name "*.md" 2>/dev/null | wc -l)
MODULE2_COUNT=$(find docs/module2 -name "*.md" 2>/dev/null | wc -l)
MODULE3_COUNT=$(find docs/module3 -name "*.md" 2>/dev/null | wc -l)
MODULE4_COUNT=$(find docs/module4 -name "*.md" 2>/dev/null | wc -l)

echo "Content file counts:"
echo "- Module 1: $MODULE1_COUNT files (expected: 6 - 5 weeks + summary + intro)"
echo "- Module 2: $MODULE2_COUNT files (expected: 3 - 2 weeks + summary)"
echo "- Module 3: $MODULE3_COUNT files (expected: 4 - 3 weeks + summary)"
echo "- Module 4: $MODULE4_COUNT files (expected: 4 - 3 weeks + summary)"
echo

# Count examples
EXAMPLES_COUNT=$(find code/examples -name "*.py" 2>/dev/null | wc -l)
echo "Example files found: $EXAMPLES_COUNT (expected: ~20)"

# Count diagrams
DIAGRAMS_COUNT=$(find diagrams -name "*.svg" 2>/dev/null | wc -l)
echo "Diagram files found: $DIAGRAMS_COUNT (expected: 12)"
echo

# Run word count validation
echo "Running word count validation..."
python scripts/check-wordcount.py
WORDCOUNT_RESULT=$?
if [ $WORDCOUNT_RESULT -eq 0 ]; then
    echo "✓ Word count validation passed"
else
    echo "✗ Word count validation failed"
fi
echo

# Run link validation
echo "Running link validation..."
bash scripts/link-check.sh
LINKCHECK_RESULT=$?
if [ $LINKCHECK_RESULT -eq 0 ]; then
    echo "✓ Link validation passed"
else
    echo "✗ Link validation failed"
fi
echo

# Run diagram validation
echo "Running diagram validation..."
bash scripts/check-diagrams.sh
DIAGRAMCHECK_RESULT=$?
if [ $DIAGRAMCHECK_RESULT -eq 0 ]; then
    echo "✓ Diagram validation passed"
else
    echo "✗ Diagram validation failed"
fi
echo

# Check for required files
echo "Checking required files..."
REQUIRED_FILES=(
    "docusaurus.config.ts"
    "sidebars.ts"
    "package.json"
    "README.md"
    "docs/intro.md"
    "docs/module1/summary.md"
    "docs/module2/summary.md"
    "docs/module3/summary.md"
    "docs/module4/summary.md"
)

MISSING_FILES=0
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file exists"
    else
        echo "✗ $file missing"
        MISSING_FILES=$((MISSING_FILES + 1))
    fi
done

echo

# Check Docusaurus configuration
if [ -f "docusaurus.config.ts" ]; then
    echo "Checking Docusaurus configuration..."
    if grep -q "Physical AI & Humanoid Robotics" docusaurus.config.ts; then
        echo "✓ Site title is correct"
    else
        echo "✗ Site title not found in docusaurus.config.ts"
    fi
fi

echo

# Final summary
TOTAL_ERRORS=0
if [ $WORDCOUNT_RESULT -ne 0 ]; then TOTAL_ERRORS=$((TOTAL_ERRORS + 1)); fi
if [ $LINKCHECK_RESULT -ne 0 ]; then TOTAL_ERRORS=$((TOTAL_ERRORS + 1)); fi
if [ $DIAGRAMCHECK_RESULT -ne 0 ]; then TOTAL_ERRORS=$((TOTAL_ERRORS + 1)); fi
if [ $MISSING_FILES -ne 0 ]; then TOTAL_ERRORS=$((TOTAL_ERRORS + 1)); fi

echo "Verification Summary:"
echo "==================="
echo "Word count check: $([ $WORDCOUNT_RESULT -eq 0 ] && echo 'PASS' || echo 'FAIL')"
echo "Link validation: $([ $LINKCHECK_RESULT -eq 0 ] && echo 'PASS' || echo 'FAIL')"
echo "Diagram validation: $([ $DIAGRAMCHECK_RESULT -eq 0 ] && echo 'PASS' || echo 'FAIL')"
echo "Missing files: $([ $MISSING_FILES -eq 0 ] && echo '0' || echo $MISSING_FILES)"
echo

if [ $TOTAL_ERRORS -eq 0 ]; then
    echo "🎉 All verifications PASSED!"
    exit 0
else
    echo "❌ $TOTAL_ERRORS verification(s) FAILED!"
    exit 1
fi