# Currency Converter

A comprehensive Python library for currency conversion with real-time exchange rates and a user-friendly CLI.

## Features

- Real-time currency conversion
- Support for multiple currencies
- Caching of exchange rates
- Fallback mechanism for rate fetching
- Flexible formatting options
- Command-line interface

## Installation

```bash
pip install currency-converter-ext
```

## Usage

### As a Library

```python
from currency_converter.main import CurrencyConverter

# Initialize converter
converter = CurrencyConverter()

# Convert currencies
result = converter.convert(100, 'USD', 'EUR')
print(result)  # Outputs converted amount
```

### CLI Usage

```bash
# Launch the CLI
currency-converter
```

## Requirements

- Python 3.7+
- requests library

## License

MIT License