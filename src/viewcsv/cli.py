from __future__ import annotations
import csv
import sys
import argparse
from pathlib import Path
from statistics import mean
from typing import List, Optional
from dataclasses import dataclass
from count_cjk import count_cjk


@dataclass
class Cell:
    """Represents a single cell in the CSV"""

    value: str

    @property
    def display_width(self) -> int:
        """
        Calculate display width by:
        1. Getting base length of string
        2. Adding 1 extra width for each CJK character
        """
        return len(self.value) + count_cjk(self.value)

    def wrap(self, width: int) -> List[str]:
        """Wrap cell content into multiple lines if it exceeds width"""
        if self.display_width <= width:
            return [self.value]

        lines = []
        current_line = ""
        current_width = 0

        for char in self.value:
            char_width = 2 if ord(char) > 0x7F else 1
            if current_width + char_width > width:
                lines.append(current_line)
                current_line = char
                current_width = char_width
            else:
                current_line += char
                current_width += char_width

        if current_line:
            lines.append(current_line)

        return lines

    def __str__(self) -> str:
        return self.value


class Row:
    """Represents a row in the CSV"""

    def __init__(self, cells: List[str]):
        self.cells = [Cell(str(value)) for value in cells]

    def __getitem__(self, index: int) -> Cell:
        return self.cells[index]

    def __len__(self) -> int:
        return len(self.cells)

    def pad_to_length(self, length: int) -> None:
        """Pad the row with empty cells"""
        while len(self) < length:
            self.cells.append(Cell(""))


class Column:
    """Represents a column in the CSV"""

    def __init__(self, index: int, rows: List[Row]):
        self.index = index
        self.cells = [row[index] for row in rows if index < len(row)]

    @property
    def width(self) -> int:
        """Get the maximum width of cells in this column"""
        if not self.cells:
            return 1
        return max(cell.display_width for cell in self.cells)

    @property
    def mean_width(self) -> float:
        """Calculate mean width of cells in this column"""
        if not self.cells:
            return 1
        return mean(cell.display_width for cell in self.cells)

    def calculate_optimal_width(self, width_multiplier: float = 2.0) -> int:
        """Calculate optimal width based on mean width"""
        if not self.cells:
            return 1

        threshold = int(self.mean_width * width_multiplier)
        max_width = max(cell.display_width for cell in self.cells)

        return threshold if max_width > threshold else max_width


class CSVContent:
    """Represents the entire CSV content"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.header: Optional[Row] = None
        self.rows: List[Row] = []
        self._read_file()

    def _read_file(self) -> None:
        """Read and parse the CSV file"""
        try:
            with self.file_path.resolve().open("r", encoding="utf-8", newline="") as f:
                reader = csv.reader(f)
                all_rows = list(reader)

                if not all_rows:
                    return

                # Get the maximum number of columns
                max_columns = max(len(row) for row in all_rows)

                # Create and pad rows
                self.rows = []
                for row_data in all_rows:
                    row = Row(row_data)
                    row.pad_to_length(max_columns)
                    self.rows.append(row)

                # Separate header
                self.header = self.rows.pop(0) if self.rows else None

        except UnicodeDecodeError:
            # Try Windows encoding
            try:
                with self.file_path.resolve().open(
                    "r", encoding="cp1252", newline=""
                ) as f:
                    reader = csv.reader(f)
                    self._process_rows(reader)
            except UnicodeDecodeError:
                print(
                    f"Error: Unable to decode file. Please ensure it's a valid CSV file with UTF-8 or ASCII encoding.",
                    file=sys.stderr,
                )
                sys.exit(1)

    @property
    def columns(self) -> List[Column]:
        """Get all columns in the CSV"""
        if not self.rows and not self.header:
            return []

        num_columns = len(self.header) if self.header else len(self.rows[0])
        all_rows = [self.header] + self.rows if self.header else self.rows
        return [Column(i, all_rows) for i in range(num_columns)]

    def print_csv(
        self,
        no_header: bool = False,
        max_rows: int = None,
        width_multiplier: float = 2.0,
    ) -> None:
        """Print the CSV content with formatted columns"""
        # Calculate optimal widths
        column_widths = [
            col.calculate_optimal_width(width_multiplier) for col in self.columns
        ]

        # Print header
        if self.header and not no_header:
            self._print_formatted_row(self.header, column_widths)
            print("-" * sum(column_widths) + "-" * (len(column_widths) * 3 - 1))

        # Print rows
        rows_to_print = self.rows[:max_rows] if max_rows else self.rows
        for row in rows_to_print:
            self._print_formatted_row(row, column_widths)

    def _print_formatted_row(self, row: Row, widths: List[int]) -> None:
        """Print a single row with proper formatting"""
        # Wrap cells
        wrapped_cells = [cell.wrap(width) for cell, width in zip(row.cells, widths)]

        # Calculate total lines needed
        max_lines = max(len(cell_lines) for cell_lines in wrapped_cells)

        # Print each line
        for line_idx in range(max_lines):
            line_parts = []
            for cell_lines, width in zip(wrapped_cells, widths):
                content = cell_lines[line_idx] if line_idx < len(cell_lines) else ""
                padding = width - len(content) - count_cjk(content)
                line_parts.append(content + " " * padding)
            cell_gap = " | " if line_idx == 0 else "   "
            print(cell_gap.join(line_parts))


def main():
    """Main entry point for the CLI"""
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

    parser.add_argument(
        "--width-multiplier",
        type=float,
        default=2.0,
        help="Multiplier for mean width to determine column width (default: 2.0)",
    )

    args = parser.parse_args()

    try:
        csv_content = CSVContent(args.file)
        csv_content.print_csv(args.no_header, args.max_rows, args.width_multiplier)
    except KeyboardInterrupt:
        print("\nViewing terminated", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
