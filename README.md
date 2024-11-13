# ViewCSV

A command-line tool for viewing CSV files with aligned columns. It makes CSV files easier to read in the terminal.

## Features

- Header row highlighting with separator lines
- Supports CJK (Chinese, Japanese, Korean) characters
- Cross-platform compatibility (Windows, Linux, macOS)
- Smart column width adjustment based on content statistics
- Intelligent text wrapping for long content
- Automatic encoding detection (UTF-8 and Windows CP1252)
- Handles irregular CSV files (varying column counts)
- Configurable display options

## Installation

```bash
pip install viewcsv
```

## Usage

```bash
viewcsv data.csv                        # View entire CSV file
viewcsv data.csv -n 10                  # View first 10 rows
viewcsv data.csv --no-header            # View without header row
viewcsv data.csv --width-multiplier 1.5 # Adjust column width threshold
```

## Advanced Options

- `--width-multiplier`: Controls column width threshold (default: 2.0)
  - Lower values (e.g., 1.5) create narrower columns with more text wrapping
  - Higher values (e.g., 3.0) allow wider columns with less wrapping
  - Based on the average width of content in each column

## Examples

Input CSV:
```csv
Name,Age,City,Description
John Smith,25,New York,A software engineer
张三,30,Beijing,数据科学家和机器学习专家
Alice Johnson,28,London,This is a very long description that will be automatically wrapped to maintain readable column widths
```

Output:
```
Name           | Age | City     | Description
------------------------------------------------
John Smith     | 25  | New York | A software engineer
张三三          | 30  | Beijing  | 数据科学家和机器学习专家
Alice Johnson  | 28  | London   | This is a very long
                                | description that will
                                | be automatically wrapped
                                | to maintain readable
                                | column widths
```

## Requirements

- Python 3.7 or higher
- No external dependencies required

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
