# AT Common Tasks

A Python package providing common asynchronous task definitions and utilities for workflow operations.

## Installation
```bash
pip install at_common_tasks
```

## Usage
```python
from at_common_workflow import Context
from at_common_tasks import echo, reverse, add_integers
async def main():
    context = Context()
    # Echo example
    context["in_msg"] = "Hello, World!"
    await echo(context)
    print(context["out_msg"]) # Outputs: Hello, World!
    
    # Add integers example
    context["num1"] = 5
    context["num2"] = 3
    await add_integers(context)
    print(context["result"]) # Outputs: 8
```

## Development

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment
4. Install development dependencies: `pip install -e ".[dev]"`
5. Run tests: `pytest`

## License

This project is licensed under the MIT License - see the LICENSE file for details.