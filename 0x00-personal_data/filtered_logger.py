#!/usr/bin/env python3
"""Personal data.

Classes:
    RedactingFormatter

Functions:
    filter_datum(fields, redaction, message, separator)
    get_logger()
    get_db()
    main()

Attributes:
    PII_FIELDS
"""
import re
from typing import List
import logging
import os
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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

    logger = logging.getLogger("user_data")
    logger.propagate = False
    logger.setLevel(logging.INFO)

    formatter = RedactingFormatter(PII_FIELDS)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connection to a given database"""

    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    conn = mysql.connector.connect(user=db_user,
                                   password=db_pwd,
                                   host=db_host,
                                   database=db_name)

    return conn


def main() -> None:
    """Reads and displays all row from the users table filtered."""

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    logger = get_logger()
    columns = cursor.column_names
    for row in cursor:
        s = " ".join("{}={};".format(k, v) for k, v in zip(columns, row))
        logger.info(s)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
