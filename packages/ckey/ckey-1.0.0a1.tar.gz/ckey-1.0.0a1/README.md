# ckey
### OpenFEC API client for researching the political ideology of executives

Copyright (c) 2024 Justin G. Davis.

## Overview
Ckey is a data collection and analysis tool that uses executive information from ExecuComp to capture political contribution data from openFEC, the Federal Election Commission (FEC) API. It allows researchers to construct measures of executive political ideology based on the executives' political contributions.

> **Disclaimer** - Ckey is not affiliated with, endorsed by, or vetted by ExecuComp.

## Features
- **User-Friendly** - Designed for researchers with minimal Python experience
- **Data Processing** - Automated cleaning and formatting of ExecuComp data
- **API Integration** - Efficient data collection from openFEC API with built-in rate limiting
- **Compliance** - Integrated adherence to openFEC API usage policies
- **Political Analysis** - Construction of all commonly used political ideology measures
- **Accurate Matching** - Robust executive-to-contribution matching using name, employer, and occupation verification

## Installation
```bash
pip install ckey
```

## Prerequisites & Dependencies

### Prerequisites
- Python 3.6 or higher
- Access to ExecuComp data
- FEC API key (obtain from [FEC.gov](https://api.open.fec.gov/developers))

### Python Dependencies
- pandas >= 2.0.0
- requests >= 2.31.0
- ThreadPoolExecutorPlus >= 0.2.2

Note: Python dependencies are automatically installed during the pip installation

## Usage Guide

### Basic Usage
```python
import ckey

ckey.run(
    data_path='your ExecuComp data.csv',
    id_column='exec id column in the data',
    name_column='name column in the data',
    company_column='company column in the data',
    year_column='year column in the data',
    key='YOUR_API_KEY'
)
```
For detailed usage instructions and methodology, please see:

[Citation information to be added]

## Citation
If you use this tool in your research, please cite:

[Citation information to be added]

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
Thank you to:
- The FEC for providing and maintaining the openFEC API.
- The openFEC support staff for their assistance throughout the development process.

## Author
Justin G. Davis
