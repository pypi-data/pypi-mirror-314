# EDGARDSRS: Tool for SEC 10-k files
| | |
| --- | --- |
| License | [![License](https://img.shields.io/badge/LICENSE-blue)](https://github.com/pratikrelekar/Edgartool/blob/main/LICENSE) |
| Dependencies | ![PyPI - Version](https://img.shields.io/pypi/v/beautifulsoup4?label=beautifulsoup4)
| Meta | 
## Description:

EDGARDSRS is a Python library designed to clean and process SEC EDGAR 10-K filing HTML files. It removes unnecessary HTML elements, various types of noise/gibberish text, and extract tables with high numeric content to produce clean, readable text output suitable for analysis.

## Features

- HTML cleaning and text extraction
- Removal of financial tables and numeric-heavy content
- Extract financial tables 
- Elimination of noisy text and gibberish
- Unicode normalization
- Special character handling
- Multiple HTML parser support (html.parser, lxml, html5lib)

## Installation

```bash
pip install edgardsrs
```

Required dependencies:
- beautifulsoup4
- lxml
- html5lib
- unicodedata

## Usage

Basic usage to clean a 10-K HTML file:

```python
from edgardsrs import EdgarDSRS

analyzer = EdgarDSRS()

# Cleaning the file
input_file = "your_10k_file.html"
cleaned_file = analyzer.process_html_file(input_file)
```

## Cleaning Process

The tool performs the following cleaning operations:

1. **HTML Parsing**: Attempts to parse HTML using multiple parsers (html.parser, lxml, html5lib)
2. **Tag Removal**: Strips all HTML tags while preserving text content
3. **Unicode Normalization**: Normalizes Unicode characters
4. **Noise Removal**:
   - Removes sequences with high special character density
   - Eliminates base64 encoded patterns
   - Cleans up lines with excessive non-alphanumeric characters
5. **Text Cleaning**:
   - Removes noisy words (mixed case with numbers, excessive length)
   - Normalizes whitespace

## Functions

### `clean_html_content(html_content)`
Main function to clean HTML content and extract text.

```python
text = EdgarDSRS.clean_html_content(html_content)
```

### `extract_and_format_tables`
Function to extract tables.

```python
soup = BeautifulSoup(html_content, "html.parser")
tables = extract_and_format_tables(soup)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Pratik Relekar | Xinyao Qian

## Background

This library was developed at [**Data Science Research Services(University of Illinois at Urbana-Champaign)**](https://dsrs.illinois.edu) in 2024 and has been under active development since then.

## Getting help

For general questions and discussions, visit [**DSRS mailing list**](https://dsrs.illinois.edu/about/faq).
