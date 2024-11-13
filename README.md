# ViewCSV

A command-line tool for viewing CSV files with aligned columns. It makes CSV files easier to read in the terminal.

## Features

- Smart column width adjustment based on content statistics
- Intelligent text wrapping for long content
- Cross-platform compatibility (Windows, Linux, macOS)
- Header row highlighting with separator lines
- Supports CJK (Chinese, Japanese, Korean) characters
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
John Smith,25,New York,Software engineer
张三,30,Beijing,数据科学家和机器学习专家
Maria García,28,Madrid,¡Desarrolladora de aplicaciones móviles!
Александр,35,Moscow,Специалист по анализу данных
김영희,27,Seoul,프로그래머 & 개발자
中村 悠太,31,Tokyo,システムエンジニア・プログラマー
Lars Müller,29,Berlin,Software-Entwickler & IT-Berater
Sophie Martin,26,Paris,Ingénieure en intelligence artificielle
王小明,33,Shanghai,高级工程师（全栈开发）〜通信系统
山田花子,28,Osaka,データサイエンティスト＆機械学習専門家
Elena Popov,31,St. Petersburg,Веб-разработчик и UX-дизайнер
李四,29,Guangzhou,全栈工程师・DevOps专家…续
Sarah Williams,27,London,This is another very very very long description that will definitely need to be wrapped into multiple lines to maintain readable formatting
洪大同,31,Taipei,資深軟體工程師（後端開發）
박지민,25,Busan,풀스택 개발자 & 소프트웨어 아키텍트
```

Output:
```
Name           | Age | City          | Description
---------------------------------------------------------------------------------------------------------------
John Smith     | 25  | New York      | Software engineer
张三            | 30  | Beijing       | 数据科学家和机器学习专家
Maria García   | 28  | Madrid        | ¡Desarrolladora de aplicaciones móviles!
Александр      | 35  | Moscow        | Специалист по анализу данных
김영희          | 27  | Seoul         | 프로그래머 & 개발자
中村 悠太       | 31  | Tokyo         | システムエンジニア・プログラマー
Lars Müller    | 29  | Berlin        | Software-Entwickler & IT-Berater
Sophie Martin  | 26  | Paris         | Ingénieure en intelligence artificielle
王小明          | 33  | Shanghai      | 高级工程师（全栈开发）〜通信系统
山田花子        | 28  | Osaka         | データサイエンティスト＆機械学習専門家
Elena Popov    | 31  | St. Petersbur | Веб-разработчик и UX-дизайнер
                       g
李四           | 29  | Guangzhou     | 全栈工程师・DevOps专家…续
Sarah Williams | 27  | London        | This is another very very very long description that will definitely n
                                       eed to be wrapped into multiple lines to maintain readable formatting
洪大同         | 31  | Taipei        | 資深軟體工程師（後端開發）
박지민         | 25  | Busan         | 풀스택 개발자 & 소프트웨어 아키텍트
```

## Requirements

- Python 3.7 or higher
- No external dependencies required

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
