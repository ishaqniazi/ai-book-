# Textbook Content Contract

## Overview
This contract defines the structure and format of the Physical AI & Humanoid Robotics textbook content. Since this is a static documentation project using Docusaurus, the "API" consists of content files following specific schemas.

## Content Schema

### Module Schema
```
{
  "id": "string (kebab-case, e.g., 'module-1-ros2')",
  "title": "string",
  "description": "string",
  "weekRange": "string (e.g., 'Weeks 1-5')",
  "wordCount": "integer",
  "targetWordCount": {
    "min": "integer",
    "max": "integer"
  },
  "content": "string (Docusaurus Markdown)",
  "frontmatter": {
    "title": "string",
    "description": "string",
    "sidebar_position": "integer",
    "tags": ["string"]
  },
  "examples": [
    {
      "id": "string",
      "title": "string",
      "path": "string (relative to /code/)"
    }
  ],
  "diagrams": [
    {
      "id": "string",
      "title": "string",
      "path": "string (relative to /diagrams/)",
      "altText": "string"
    }
  ]
}
```

### Example Schema
```
{
  "id": "string (e.g., 'example-1-module-1')",
  "moduleId": "string",
  "title": "string",
  "description": "string",
  "language": "string (e.g., 'python', 'cpp')",
  "path": "string (relative path to example)",
  "requiresGPU": "boolean",
  "dependencies": ["string"],
  "environment": "Ubuntu 22.04",
  "hasTypeHints": "boolean",
  "hasErrorHandling": "boolean",
  "commentsLanguage": "English"
}
```

### Diagram Schema
```
{
  "id": "string (e.g., 'diagram-1-module-1')",
  "moduleId": "string",
  "title": "string",
  "altText": "string",
  "caption": "string",
  "format": "'SVG' | 'PNG'",
  "path": "string (relative path to diagram)",
  "accessibilityCompliant": "boolean"
}
```

## Endpoints (File Structure)

### Module Content
- **Path**: `/docs/module-{number}-{name}/index.md`
- **Method**: GET (file read)
- **Response**: Docusaurus Markdown with frontmatter
- **Content-Type**: text/markdown

### Example Code
- **Path**: `/code/module-{number}/example-{number}/`
- **Method**: GET (directory access)
- **Response**: Code files, requirements, test scripts
- **Content-Type**: application/octet-stream (for files)

### Diagrams
- **Path**: `/diagrams/module-{number}/diagram-{number}.{format}`
- **Method**: GET (file read)
- **Response**: Image file
- **Content-Type**: image/svg+xml | image/png

## Validation Rules

### Content Validation
- Word count must be within specified range per module
- All code examples must run in Ubuntu 22.04
- All examples must include type hints
- All examples must include English comments
- All examples must include basic error handling
- All diagrams must have alt text
- All content must meet WCAG 2.1 AA standards

### Format Validation
- Markdown files must follow Docusaurus format with proper frontmatter
- Code files must include proper licensing and attribution
- Diagrams must be in SVG or PNG format
- Example metadata must be in `examples/meta.yaml`
- Diagram metadata must be in `diagrams/meta.yaml`

## Error Handling

Since this is a static content project:
- Missing content results in 404 errors
- Invalid formats cause Docusaurus build failures
- Accessibility issues result in validation script failures
- Broken links are detected by link-check script

## Versioning
- Content versioning follows Git repository tags
- Schema versioning is tracked in this contract document
- Breaking changes to content structure require new major version