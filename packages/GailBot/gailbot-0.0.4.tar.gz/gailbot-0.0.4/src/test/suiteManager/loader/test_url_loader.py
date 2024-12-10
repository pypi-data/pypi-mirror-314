import os
import unittest

from gailbot.pluginSuiteManager.pluginSuiteManager import PluginSuiteManager
from gailbot.pluginSuiteManager.suiteLoader import PluginURLSuiteLoader
from gailbot.shared.utils.general import delete, make_dir
from test.suiteManager import SUITE_TEST_SRC_PATH, SUITE_TEST_WORKSPACE_PATH


class MyTestCase(unittest.TestCase):
    plugin_suite_manager = PluginSuiteManager(SUITE_TEST_WORKSPACE_PATH)
    src_root = SUITE_TEST_SRC_PATH
    suite_ws = os.path.join(SUITE_TEST_WORKSPACE_PATH, "suites")
    download_ws = os.path.join(SUITE_TEST_WORKSPACE_PATH, "download")
    f = open(os.path.join(SUITE_TEST_WORKSPACE_PATH, "log.txt"), "w+")

    def test_load_invalid(self):
        loader = PluginURLSuiteLoader(self.download_ws, self.suite_ws)
        assert not loader.load("invalid-url", self.f)

    def test_zip_url(self):
        url = "https://gailbot-plugin-suite-official.s3.us-east-2.amazonaws.com/HiLabSuite.zip"
        delete(self.download_ws)
        delete(self.suite_ws)
        make_dir(self.download_ws)
        make_dir(self.suite_ws)
        assert self.plugin_suite_manager.register_suite(url)

    def test_bucket(self):
        bucket = "gailbot-plugin-suite-official"
        delete(self.download_ws)
        delete(self.suite_ws)
        make_dir(self.download_ws)
        make_dir(self.suite_ws)
        assert self.plugin_suite_manager.register_suite(bucket)


if __name__ == '__main__':
    unittest.main()
