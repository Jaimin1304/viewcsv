# ViewCSV

A command-line tool for viewing CSV files with aligned columns. It automatically adjusts column widths based on content, making CSV files easier to read in the terminal.

## Features

- Automatically aligns columns based on content width
- Supports CJK (Chinese, Japanese, Korean) characters
- Cross-platform compatibility (Windows, Linux, macOS)
- Header row highlighting
- Configurable display options

## Installation

```bash
pip install viewcsv
```

## Usage

```bash
viewcsv data.csv                 # View entire CSV file
viewcsv data.csv -n 10          # View first 10 rows
viewcsv data.csv --no-header    # View without header row
```

## Examples

Input CSV:

```csv
Name,Age,City
John Smith,25,New York
张三,30,Beijing
```

Output:

```
Name       | Age | City
-----------------------
John Smith | 25  | New York
张三       | 30  | Beijing
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
