def escape_special_characters(text):
    special_characters_dict = {
        '+': '"plus"',
        '-': '"minus"',
        '*': '"asterisk"',
        ':': '"colon"',
        '(': '"leftparen"',
        ')': '"rightparen"',
        '[': '"leftbracket"',
        ']': '"rightbracket"',
        '{': '"leftbrace"',
        '}': '"rightbrace"',
        '~': '"tilde"',
        '?': '"questionmark"',
        '\\': '"backslash"'
    }
    
    for char, replacement in special_characters_dict.items():
        text = text.replace(char, replacement)
    
    return text

def return_special_characters(text):
    special_characters_dict = {
        '"plus"': '+',
        '"minus"': '-',
        '"asterisk"': '*',
        '"colon"': ':',
        '"leftparen"': '(',
        '"rightparen"': ')',
        '"leftbracket"': '[',
        '"rightbracket"': ']',
        '"leftbrace"': '{',
        '"rightbrace"': '}',
        '"tilde"': '~',
        '"questionmark"': '?',
        '"backslash"': '\\'
    }

    for char, replacement in special_characters_dict.items():
        text = text.replace(char, replacement)

    return text
