import unittest

from gailbot.shared.exception.serviceException import EngineAddError, DuplicateProfile
from gailbot.shared.exception.transcribeException import InternetConnectionError


class MyTestCase(unittest.TestCase):
    def test_exception(self):
        try:
            raise InternetConnectionError()
        except Exception as e:
            print(e)
            assert isinstance(e, InternetConnectionError)

    def test_add_exception(self):
        try:
            raise EngineAddError("test", cause=Exception())
        except Exception as e:
            print(e)
            assert isinstance(e, EngineAddError)

    def test_duplicate_exception(self):
        try:
            raise DuplicateProfile("test")
        except Exception as e:
            print(e)
            assert isinstance(e, DuplicateProfile)


if __name__ == '__main__':
    unittest.main()
