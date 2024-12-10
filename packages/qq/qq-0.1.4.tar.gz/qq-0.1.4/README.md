# Quick Question (qq)

A command-line tool that suggests and executes terminal commands using various LLM providers. It prioritizes local LLM providers for privacy and cost efficiency, with fallback to cloud providers when configured. This tool is still under development and initally tested in MacOS, we'll continue expanding as we receive feedback, please feel free to reach out with ideas and feedback to cv@southbrucke.com

## Features

- Multiple LLM provider support:
  - Local providers (prioritized):
    - LM Studio
    - Ollama
  - Cloud providers (requires API keys):
    - OpenAI
    - Anthropic
    - Groq
- Interactive command selection
- Command history tracking
- Configurable settings
- Copy to clipboard or direct execution options
- macOS-optimized command suggestions

## Installation

```bash
pip install qq
```

## Usage

Basic command:
```bash
qq "your question here"
```

Configure settings:
```bash
qq --settings
```

View command history:
```bash
qq
```

## Provider Selection

The tool follows this priority order for LLM providers:

1. Checks for running local providers (LM Studio or Ollama)
2. If no local providers are available, checks for configured cloud provider API tokens
3. Uses the first available provider unless a specific default is set in settings

## Configuration

Use `qq --settings` to configure:
- Default provider selection
- Command action (execute or copy to clipboard)
- Default model for each provider
- API keys for cloud providers

## Environment Variables

Cloud provider API keys can be set via environment variables:
- `OPENAI_API_KEY` - for OpenAI
- `ANTHROPIC_API_KEY` - for Anthropic
- `GROQ_API_KEY` - for Groq

## Examples

Get file search commands:
```bash
qq "how do I search for files containing specific text"
```

Find process information:
```bash
qq "show me all running processes containing 'python'"
```

## Requirements

- Python >= 3.6
- macOS (optimized for macOS terminal commands)
- Local LLM provider (LM Studio or Ollama) or cloud provider API key

## License

Proprietary - All rights reserved

## Author

Cristian Vyhmeister (cv@southbrucke.com)

For more information, visit [https://southbrucke.com](https://southbrucke.com)