# utilyzer 

A tool for awesome python utils

[![PyPI version](https://badge.fury.io/py/utilyzer.svg)](https://badge.fury.io/py/utilyzer)
[![ci-cd](https://github.com/asmitul/utilyzer/actions/workflows/ci-cd.yaml/badge.svg)](https://github.com/asmitul/utilyzer/actions/workflows/ci-cd.yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/utilyzer)](https://pypi.org/project/utilyzer)
[![PyPI Downloads](https://img.shields.io/pypi/dm/utilyzer)](https://pypi.org/project/utilyzer)

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

- Date utilities with support for:
  - Getting day ranges with timestamps
  - Timezone awareness
  - Flexible day lookback

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

## Date Utilities

```python
from utilyzer import get_day_range

# Get today's range
today = get_day_range()

# Get yesterday's range
yesterday = get_day_range(1)

# Get range with different timezone
hk_time = get_day_range(0, timezone='Asia/Hong_Kong')
```

## Requirements

- Python >= 3.8
- Python < 3.12

## Development on local, check code quality

```bash
# First review the changes
black --check --diff --preview src tests

# Then apply them if you're happy with the proposed changes
black --preview src tests

# Check ruff
ruff check src tests

# Fix ruff
ruff check --fix src tests

# Check mypy
mypy src
```

## Documentation

Full documentation is available at [https://asmitul.github.io/utilyzer](https://asmitul.github.io/utilyzer)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- **asmitul** - [GitHub](https://github.com/asmitul)