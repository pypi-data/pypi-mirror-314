def chinese_to_rtf(chinese_text):
    rtf_body = ''.join(
        [f'\\u{ord(char)};' if ord(char) > 127 else char for char in chinese_text]
    )
    rtf_body = f"{{\\cf0\\b {rtf_body} \\b0\\tab}}"
    return rtf_body