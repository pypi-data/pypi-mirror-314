# utilyzer

A tool for awesome python utils

[![PyPI version](https://badge.fury.io/py/utilyzer.svg)](https://badge.fury.io/py/utilyzer)
[![ci-cd](https://github.com/asmitul/utilyzer/actions/workflows/ci-cd.yaml/badge.svg)](https://github.com/asmitul/utilyzer/actions/workflows/ci-cd.yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation

```bash
pip install utilyzer
```

## Features

- String to Number conversion with support for:
  - Integer conversion
  - Float conversion
  - Scientific notation
  - Whitespace handling
  - Robust error handling

## Quick Start

```python
from utilyzer import str_to_number

# Convert string to integer
str_to_number("123") # 123  

# Convert string to float
str_to_number("12.34") # 12.34

# Convert string to scientific notation
str_to_number("1e-10") # 1e-10

# Handle whitespace
str_to_number("  123  ") # 123

# Handle invalid input
str_to_number("abc") # None

# Handle empty string
str_to_number("") # None

# Handle None
str_to_number(None) # None
```

## Requirements

- Python >= 3.8
- Python < 3.12


## Documentation

Full documentation is available at [https://asmitul.github.io/utilyzer](https://asmitul.github.io/utilyzer)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- **asmitul** - [GitHub](https://github.com/asmitul)