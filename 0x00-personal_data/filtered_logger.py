#!/usr/bin/env python3
"""Personal data.
Regex-ing

Functions:
    filter_datum(fields, redaction, message, separator)
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """"Returns a log message obfuscated."""
    pattern = f'({"|".join([f+"=" for f in fields])})([^{separator}]+)'
    return re.sub(pattern, r'\1' + redaction, message)
