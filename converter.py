import re


def to_uppercase(text):
    return text.upper()


def to_lowercase(text):
    return text.lower()


def to_title_case(text):
    return text.title()


def to_sentence_case(text):
    text = text.lower()
    sentences = re.split(r'([.!?]\s*)', text)
    result = []
    for s in sentences:
        if s.strip() and not re.match(r'^[.!?]\s*$', s):
            s = s[0].upper() + s[1:] if s else s
        result.append(s)
    return "".join(result)


def to_camel_case(text):
    words = re.findall(r'[A-Za-z0-9]+', text)
    if not words:
        return ""
    result = words[0].lower()
    for word in words[1:]:
        result += word.capitalize()
    return result


def to_pascal_case(text):
    words = re.findall(r'[A-Za-z0-9]+', text)
    return "".join(word.capitalize() for word in words)


def to_snake_case(text):
    words = re.findall(r'[A-Za-z0-9]+', text)
    return "_".join(word.lower() for word in words)


def to_constant_case(text):
    words = re.findall(r'[A-Za-z0-9]+', text)
    return "_".join(word.upper() for word in words)


def to_kebab_case(text):
    words = re.findall(r'[A-Za-z0-9]+', text)
    return "-".join(word.lower() for word in words)


def to_alternating_case(text):
    result = []
    for i, char in enumerate(text):
        if char.isalpha():
            result.append(char.upper() if i % 2 == 0 else char.lower())
        else:
            result.append(char)
    return "".join(result)


def to_inverse_case(text):
    return "".join(c.lower() if c.isupper() else c.upper() for c in text)


def remove_extra_spaces(text):
    return re.sub(r'\s+', ' ', text).strip()


def to_reverse(text):
    return text[::-1]


CONVERSIONS = [
    ("MAYÚSCULAS", to_uppercase, "HOLA MUNDO"),
    ("minúsculas", to_lowercase, "hola mundo"),
    ("Title Case", to_title_case, "Hola Mundo"),
    ("Sentence case", to_sentence_case, "Hola mundo."),
    ("camelCase", to_camel_case, "holaMundo"),
    ("PascalCase", to_pascal_case, "HolaMundo"),
    ("snake_case", to_snake_case, "hola_mundo"),
    ("CONSTANT_CASE", to_constant_case, "HOLA_MUNDO"),
    ("kebab-case", to_kebab_case, "hola-mundo"),
    ("aLtErNaTiNg CaSe", to_alternating_case, "HoLa MuNdO"),
    ("InVeRsE cAsE", to_inverse_case, "hOLA mUNDO"),
    ("Quitar espacios extra", remove_extra_spaces, "Hola mundo"),
    ("Texto invertido", to_reverse, "odnum aloH"),
]


def get_stats(text):
    lines = text.count("\n") + 1 if text else 0
    words = len(text.split())
    chars = len(text)
    chars_no_spaces = len(text.replace(" ", "").replace("\n", ""))
    return {
        "lines": lines,
        "words": words,
        "chars": chars,
        "chars_no_spaces": chars_no_spaces
    }