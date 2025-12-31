#!/bin/bash

# Link Validation Script
# This script validates that all markdown files have valid internal links

set -e

echo "Link Validation Script"
echo "======================"

# Find all markdown files
MARKDOWN_FILES=$(find docs -name "*.md" -type f)

if [ -z "$MARKDOWN_FILES" ]; then
    echo "No markdown files found in docs directory"
    exit 1
fi

echo "Found markdown files:"
echo "$MARKDOWN_FILES"
echo

EXIT_CODE=0

# Check each markdown file for broken links
for file in $MARKDOWN_FILES; do
    echo "Checking $file..."

    # Extract internal links (relative paths, anchors, etc.)
    # This regex looks for [text](link) patterns
    if grep -E '\[.*\]\(([^)]+)\)' "$file" > /dev/null; then
        # Get all links from the file
        LINKS=$(grep -Eo '\[.*\]\(([^)]+)\)' "$file" | sed 's/.*\[(.*)\](\(.*\))/\2/')

        while IFS= read -r link; do
            # Skip external links (those starting with http, https, ftp)
            if [[ $link =~ ^https?:// ]] || [[ $link =~ ^ftp:// ]]; then
                continue
            fi

            # Remove fragment identifiers (e.g., #section)
            clean_link=$(echo "$link" | sed 's/#.*//')

            # Skip empty links
            if [ -z "$clean_link" ]; then
                continue
            fi

            # If it's an anchor link (just #something), skip for now
            if [[ $clean_link == \#* ]]; then
                continue
            fi

            # Build target path relative to the current file
            dir=$(dirname "$file")
            target="$dir/$clean_link"

            # If it starts with /, it's relative to docs root
            if [[ $clean_link == /* ]]; then
                target="docs${clean_link}"
            fi

            # Check if target exists
            if [ ! -f "$target" ]; then
                echo "  ✗ BROKEN LINK: $link in $file"
                EXIT_CODE=1
            else
                echo "  ✓ Valid: $link"
            fi
        done < <(grep -Eo '\[.*\]\(([^)]+)\)' "$file" | sed 's/.*\[(.*)\](\(.*\))/\2/')
    else
        echo "  No links found"
    fi
done

echo
if [ $EXIT_CODE -eq 0 ]; then
    echo "All links are valid!"
    exit 0
else
    echo "Some links are broken!"
    exit 1
fi