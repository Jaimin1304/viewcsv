#!/usr/bin/env python3

import csv
import argparse
from typing import List, Tuple
import sys
from pathlib import Path


def get_column_widths(csv_data: List[List[str]]) -> List[int]:
    """Calculate the maximum width for each column"""
    if not csv_data:
        return []

    # Consider display width for CJK characters
    def display_width(s: str) -> int:
        width = 0
        for char in s:
            width += 2 if ord(char) > 0x7F else 1
        return width

    num_columns = len(csv_data[0])
    widths = [0] * num_columns

    for row in csv_data:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], display_width(str(cell)))

    return widths


def format_row(row: List[str], widths: List[int]) -> str:
    """Format a single row of data with proper padding"""

    def pad_cell(cell: str, width: int) -> str:
        display_width = sum(2 if ord(c) > 0x7F else 1 for c in cell)
        padding = width - display_width
        return cell + " " * padding

    formatted_cells = [pad_cell(str(cell), width) for cell, width in zip(row, widths)]
    return " | ".join(formatted_cells)


def read_csv(file_path: str) -> Tuple[List[str], List[List[str]]]:
    """Read CSV file and return header and data"""
    # Convert string path to Path object for cross-platform compatibility
    path = Path(file_path)

    try:
        # Path.resolve() will handle path normalization across platforms
        with path.resolve().open("r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            header = next(reader)
            data = list(reader)
            return header, data
    except FileNotFoundError:
        print(f"Error: File '{path}' not found", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied accessing '{path}'", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        # Try to handle different encodings common in Windows
        try:
            with path.resolve().open("r", encoding="cp1252", newline="") as f:
                reader = csv.reader(f)
                header = next(reader)
                data = list(reader)
                return header, data
        except UnicodeDecodeError:
            print(
                f"Error: Unable to decode file. Please ensure it's a valid CSV file with UTF-8 or ASCII encoding.",
                file=sys.stderr,
            )
            sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}", file=sys.stderr)
        sys.exit(1)


def view_csv(file_path: str, no_header: bool = False, max_rows: int = None) -> None:
    """Main function to display CSV file with aligned columns"""
    header, data = read_csv(file_path)

    if max_rows:
        data = data[:max_rows]

    # Calculate column widths
    all_rows = [header] + data if not no_header else data
    widths = get_column_widths(all_rows)

    # Print header
    if not no_header:
        print(format_row(header, widths))
        print("-" * sum(widths) + "-" * (len(widths) * 3 - 1))

    # Print data rows
    for row in data:
        print(format_row(row, widths))


def main():
    parser = argparse.ArgumentParser(
        description="View CSV files with formatted and aligned columns.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "file",
        type=str,
        help="Path to the CSV file to view (supports both Windows and Unix-style paths)",
    )
    parser.add_argument(
        "--no-header", action="store_true", help="Do not display the header row"
    )
    parser.add_argument(
        "-n", "--max-rows", type=int, help="Maximum number of rows to display"
    )

    args = parser.parse_args()

    try:
        view_csv(args.file, args.no_header, args.max_rows)
    except KeyboardInterrupt:
        print("\nViewing terminated", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
