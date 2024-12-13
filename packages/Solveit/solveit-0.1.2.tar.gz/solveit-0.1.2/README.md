# Solveit

[![PyPI version](https://badge.fury.io/py/Solveit.svg)](https://badge.fury.io/py/Solveit)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Python toolkit for data processing and problem-solving.

## Features

- **Data Cleaning**: Advanced tools for handling missing values, outliers, and duplicates
- **Unit Conversion**: Comprehensive unit conversion system
- **Pathfinding**: Implementation of various pathfinding algorithms
- **Financial Calculations**: Tools for financial computations
- **Time Management**: Scheduling and timeline optimization
- **Visualization**: Easy-to-use plotting utilities

## Installation

```bash
pip install Solveit
```

## Usage Examples

### Data Cleaning
```python
from solveit.data.cleaner import DataCleaner
import pandas as pd

# Create sample data
data = {
    'Name': ['John', 'Jane', 'John', None, 'Bob'],
    'Age': [25, 30, 25, None, 100],
    'Salary': [50000, None, 50000, 60000, 1000000]
}
df = pd.DataFrame(data)

# Initialize cleaner
cleaner = DataCleaner()

# Clean the data
cleaned_df = cleaner.process_file(
    input_path='data.csv',
    output_path='cleaned_data.csv',
    operations=[
        ('remove_duplicates', {}),
        ('handle_missing_values', {'strategy': 'mean'}),
        ('remove_outliers', {'columns': ['Age', 'Salary']})
    ]
)
```

### Unit Conversion
```python
from solveit.units.converter import UnitConverter, UnitType

converter = UnitConverter()

# Convert kilometers to miles
miles = converter.convert(100, "km", "mile", UnitType.LENGTH)
print(f"100 km = {miles:.2f} miles")

# Convert Celsius to Fahrenheit
fahrenheit = converter.convert(0, "C", "F", UnitType.TEMPERATURE)
print(f"0°C = {fahrenheit}°F")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

- **Kashyapsinh Gohil** - [GitHub](https://github.com/KashyapSinh-Gohil)
- Email: k.agohil000@gmail.com

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.