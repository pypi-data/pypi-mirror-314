from abc import ABC


class GBException(ABC, Exception):
    """
    abstract class for GB exception
    """

    def __init__(self):
        self.code = 0
        self.error_msg: str = ""

    def __str__(self):
        return f"ERROR: {self.code} {self.error_msg}"
