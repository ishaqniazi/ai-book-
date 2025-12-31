#!/usr/bin/env python3
"""
Word Count Validation Script

This script validates that all module content meets the required word counts:
- Module 1: 4,000-5,000 words
- Module 2: 3,500-4,500 words
- Module 3: 4,000-5,000 words
- Module 4: 3,500-4,500 words
- Total: 15,000-20,000 words
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, Tuple


def count_words_in_file(file_path: Path) -> int:
    """Count words in a markdown file, excluding frontmatter and code blocks."""
    try:
        content = file_path.read_text(encoding='utf-8')

        # Remove frontmatter if present
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                content = parts[2]

        # Remove code blocks (both ``` and ~~~)
        content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        content = re.sub(r'~~~.*?~~~', '', content, flags=re.DOTALL)

        # Remove inline code
        content = re.sub(r'`[^`]*`', '', content)

        # Remove markdown formatting but keep the text
        content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)  # Bold
        content = re.sub(r'\*(.*?)\*', r'\1', content)      # Italic
        content = re.sub(r'__(.*?)__', r'\1', content)      # Bold
        content = re.sub(r'_(.*?)_', r'\1', content)        # Italic
        content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)  # Links
        content = re.sub(r'!\[([^\]]*)\]\([^)]+\)', '', content)    # Images

        # Remove headers and list markers
        content = re.sub(r'^#+\s+', '', content, flags=re.MULTILINE)
        content = re.sub(r'^\s*[-*+]\s+', '', content, flags=re.MULTILINE)
        content = re.sub(r'^\s*\d+\.\s+', '', content, flags=re.MULTILINE)

        # Split on whitespace and count non-empty words
        words = [word for word in re.split(r'\s+', content) if word.strip()]
        return len(words)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0


def get_module_files() -> Dict[str, list]:
    """Get all markdown files organized by module."""
    modules = {
        'module1': [],
        'module2': [],
        'module3': [],
        'module4': [],
    }

    docs_dir = Path('docs')
    if not docs_dir.exists():
        print("Error: docs directory not found")
        return modules

    for file_path in docs_dir.rglob('*.md'):
        if 'module1' in file_path.parts:
            modules['module1'].append(file_path)
        elif 'module2' in file_path.parts:
            modules['module2'].append(file_path)
        elif 'module3' in file_path.parts:
            modules['module3'].append(file_path)
        elif 'module4' in file_path.parts:
            modules['module4'].append(file_path)

    return modules


def validate_word_counts() -> Tuple[bool, Dict]:
    """Validate word counts against requirements."""
    modules = get_module_files()
    results = {}
    total_words = 0

    # Define requirements
    requirements = {
        'module1': (4000, 5000),
        'module2': (3500, 4500),
        'module3': (4000, 5000),
        'module4': (3500, 4500),
    }

    print("Word Count Validation")
    print("=" * 50)

    for module, files in modules.items():
        if not files:
            print(f"{module}: NO FILES FOUND")
            results[module] = {'count': 0, 'valid': False, 'files': []}
            continue

        module_count = 0
        file_counts = []

        for file_path in files:
            word_count = count_words_in_file(file_path)
            module_count += word_count
            file_counts.append((str(file_path), word_count))
            print(f"  {file_path.name}: {word_count} words")

        min_req, max_req = requirements.get(module, (0, float('inf')))
        valid = min_req <= module_count <= max_req
        results[module] = {
            'count': module_count,
            'valid': valid,
            'files': file_counts,
            'range': (min_req, max_req)
        }

        status = "✓" if valid else "✗"
        print(f"{module}: {module_count} words ({min_req}-{max_req} required) {status}")
        print()

        total_words += module_count

    # Check total
    total_valid = 15000 <= total_words <= 20000
    results['total'] = {
        'count': total_words,
        'valid': total_valid,
        'range': (15000, 20000)
    }

    print(f"TOTAL: {total_words} words (15,000-20,000 required) {'✓' if total_valid else '✗'}")

    return all(result['valid'] for result in results.values()), results


def main():
    """Main function to run word count validation."""
    success, results = validate_word_counts()

    if not success:
        print("\nValidation FAILED!")
        sys.exit(1)
    else:
        print("\nValidation PASSED!")
        sys.exit(0)


if __name__ == "__main__":
    main()