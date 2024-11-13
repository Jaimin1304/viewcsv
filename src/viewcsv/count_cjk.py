def count_cjk(text: str) -> int:
    """
    Count the exact number of CJK characters and punctuation in a string.

    Args:
        text: Input string that may contain CJK characters and punctuation

    Returns:
        Number of CJK characters and punctuation found

    Examples:
        >>> count_cjk("Hello世界")        # 2
        >>> count_cjk("你好，世界！")      # 5 (3个汉字 + 2个中文标点)
        >>> count_cjk("こんにちは。")      # 6 (5个假名 + 1个中文句号)
        >>> count_cjk("안녕하세요？")      # 6 (5个谚文 + 1个中文问号)
    """

    def is_cjk(char: str) -> bool:
        code = ord(char)

        # Define exact CJK Unicode ranges
        ranges = [
            # Chinese, Japanese Kanji, Korean Hanja
            (0x4E00, 0x9FFF),  # CJK Unified Ideographs
            (0x3400, 0x4DBF),  # CJK Unified Ideographs Extension A
            (0x20000, 0x2A6DF),  # CJK Unified Ideographs Extension B
            (0x2A700, 0x2B73F),  # CJK Unified Ideographs Extension C
            (0x2B740, 0x2B81F),  # CJK Unified Ideographs Extension D
            (0x2B820, 0x2CEAF),  # CJK Unified Ideographs Extension E
            (0x2CEB0, 0x2EBEF),  # CJK Unified Ideographs Extension F
            # Japanese-specific
            (0x3040, 0x309F),  # Hiragana
            (0x30A0, 0x30FF),  # Katakana
            (0x31F0, 0x31FF),  # Katakana Phonetic Extensions
            # Korean-specific
            (0xAC00, 0xD7AF),  # Hangul Syllables
            (0x1100, 0x11FF),  # Hangul Jamo
            (0x3130, 0x318F),  # Hangul Compatibility Jamo
            # CJK Punctuation and Symbols
            (0x3000, 0x303F),  # CJK Symbols and Punctuation
            (0xFF00, 0xFFEF),  # Halfwidth and Fullwidth Forms
            (0xFE30, 0xFE4F),  # CJK Compatibility Forms
            (0xFE10, 0xFE1F),  # Vertical Forms
            # Additional punctuation used in CJK texts
            (0x2018, 0x201F),  # Quotation marks (''"")
            (0x2014, 0x2015),  # Dashes (— ―)
            (0x2026, 0x2026),  # Ellipsis (…)
        ]

        return any(start <= code <= end for start, end in ranges)

    return sum(1 for char in text if is_cjk(char))


# test cases
if __name__ == "__main__":
    test_cases = [
        ("Hello world", 0),  # 纯英文
        ("Hello 世界", 2),  # 英文 + 中文
        ("你好，世界！", 5),  # 中文 + 中文标点
        ("中文：标点。符号？", 7),  # 中文 + 多种标点
        ("こんにちは。", 6),  # 日文 + 句号
        ("コンニチハ！", 6),  # 片假名 + 叹号
        ("안녕하세요？", 6),  # 韩文 + 问号
        ("你好，세상！", 4),  # 中文 + 韩文 + 标点
        ("『日本語』", 5),  # 日文 + 引号
        ("「中文」", 4),  # 中文 + 书名号
        ("Hello··世界…", 4),  # 英文 + 中文 + 特殊标点
        ("これは、テストです。", 9),  # 日文 + 多个标点
    ]

    for text, expected in test_cases:
        result = count_cjk(text)
        print(f"{text}: {result} CJK characters and punctuation (expected: {expected})")
