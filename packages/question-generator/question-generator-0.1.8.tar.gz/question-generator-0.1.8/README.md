# Prompt Generator

A Python package for generating structured prompts from markdown templates.

## Installation

```bash
pip install prompt-generator
```

## Usage

```python
from prompt_generator import PromptGenerator

# Initialize the generator
generator = PromptGenerator()

# Generate a prompt from a markdown template
prompt = await generator.generate_prompt("templates/background.md", "prompts")
```

## Features

- Generate structured prompts from markdown templates
- Support for examples and context in templates
- AWS Bedrock integration for AI-powered prompt generation
- Async/await support for efficient processing

## License

This project is licensed under the MIT License - see the LICENSE file for details.
