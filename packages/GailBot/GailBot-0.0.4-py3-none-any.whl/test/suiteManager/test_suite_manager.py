import os
import unittest

from gailbot.pluginSuiteManager.pluginSuiteManager import PluginSuiteManager
from test.suiteManager import SUITE_TEST_WORKSPACE_PATH, SUITE_TEST_SRC_PATH


class TestSuiteManager(unittest.TestCase):
    under_test = PluginSuiteManager(SUITE_TEST_WORKSPACE_PATH)

    def test_report_error(self):
        self.under_test.register_suite(os.path.join(SUITE_TEST_SRC_PATH, "MissingFiles"))
        error = self.under_test.report_registration_err(os.path.join(SUITE_TEST_SRC_PATH, "MissingFiles"))
        print(error)

        self.under_test.register_suite(os.path.join(SUITE_TEST_SRC_PATH, "NameNotFound"))
        error = self.under_test.report_registration_err(os.path.join(SUITE_TEST_SRC_PATH, "NameNotFound"))
        print(error)

        self.under_test.register_suite(os.path.join(SUITE_TEST_SRC_PATH, "UnresolvedDependency"))
        error = self.under_test.report_registration_err(os.path.join(SUITE_TEST_SRC_PATH, "UnresolvedDependency"))
        print(error)




if __name__ == '__main__':
    unittest.main()
