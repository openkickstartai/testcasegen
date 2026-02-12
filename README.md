# TestCaseGen

Automated test case generation tool that analyzes Python code and generates comprehensive test cases based on user-defined parameters. Reduces manual effort and improves test coverage through intelligent code analysis.

## Features

- **Code Analysis**: Automatically parses Python code to identify functions, classes, and their signatures
- **Multiple Framework Support**: Generates tests for pytest and unittest frameworks
- **Customizable Templates**: Flexible template system for different testing patterns
- **Intelligent Test Generation**: Creates basic, edge case, and error condition tests
- **Configuration Management**: JSON-based configuration for customizing generation behavior
- **CLI Interface**: Easy-to-use command-line interface for batch processing

## Installation

```bash
pip install -e .
```

## Quick Start

```bash
# Generate tests for a single file
python -m testcasegen.cli my_module.py

# Generate tests for an entire directory
python -m testcasegen.cli src/ -o tests/

# Use unittest framework instead of pytest
python -m testcasegen.cli my_module.py -f unittest

# Use custom configuration
python -m testcasegen.cli my_module.py -c config.json
```

## Configuration

Create a `testcasegen.json` configuration file:

```json
{
  "framework": "pytest",
  "output_dir": "tests",
  "verbose": true,
  "max_test_cases": 10,
  "include_edge_cases": true,
  "include_error_cases": true,
  "exclude_patterns": ["__*", "test_*"]
}
```

## Example

Given a Python file `calculator.py`:

```python
def add(a, b):
    """Add two numbers."""
    return a + b

def divide(a, b):
    """Divide two numbers."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

TestCaseGen will generate comprehensive test files with multiple test cases covering normal operation, edge cases, and error conditions.

## Architecture

- `analyzer.py`: Code analysis and AST parsing
- `generator.py`: Test case generation logic
- `templates.py`: Framework-specific test templates
- `config.py`: Configuration management
- `cli.py`: Command-line interface

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.