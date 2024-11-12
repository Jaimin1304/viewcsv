from viewcsv.cli import get_column_widths, format_row
import pytest


def test_get_column_widths():
    data = [
        ["Name", "Age", "City"],
        ["John", "25", "New York"],
        ["张三三", "30", "Beijing"],
    ]
    expected = [6, 3, 8]  # 考虑到中文字符宽度
    assert get_column_widths(data) == expected


def test_format_row():
    row = ["Name", "Age", "City"]
    widths = [8, 3, 8]
    expected = "Name     | Age | City    "
    assert format_row(row, widths) == expected


def test_empty_data():
    assert get_column_widths([]) == []


def test_chinese_characters():
    row = ["张三", "30", "Beijing"]
    widths = [8, 3, 8]
    expected = "张三     | 30  | Beijing "
    assert format_row(row, widths) == expected
