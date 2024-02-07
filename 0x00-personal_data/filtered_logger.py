#!/usr/bin/env python3
"""Personal data.

Classes:
    RedactingFormatter

Functions:
    filter_datum(fields, redaction, message, separator)
    get_logger()

Attributes:
    PII_FIELDS
"""
import re
from typing import List
import logging

PII_FIELDS = ("email", "phone", "ssn", "password", "ip")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """"Returns a log message obfuscated."""
    pattern = f'({"|".join([f+"=" for f in fields])})([^{separator}]+)'
    return re.sub(pattern, r'\1' + redaction, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Returns the formatted, obfuscated log message."""
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, message,
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Returns a logger that obfuscates certain given fields"""

    logger = logging.get_logger("user_data")
    logger.setLevel(logging.INFO)

    formatter = RedactingFormatter(PII_FIELDS)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
