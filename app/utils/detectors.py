import re

CALC_REGEX = re.compile(
    r"(\d+\s*[\+\-\*\/]\s*\d+)|(\b(sqrt|raiz|log|sen|cos|tan|exp|fatorial)\b)|(\d+\s*\^\s*\d+)"
)

def is_math_expression(msg: str) -> bool:
    return bool(CALC_REGEX.search(msg.lower()))