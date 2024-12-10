import os
import unittest

from gailbot.pluginSuiteManager.suiteLoader import PluginDirectorySuiteLoader
from gailbot.shared.utils.general import paths_in_dir, get_name, delete
from test.suiteManager import SUITE_TEST_SRC_PATH, SUITE_TEST_WORKSPACE_PATH


class TestDirectoryLoader(unittest.TestCase):
    src_root = SUITE_TEST_SRC_PATH
    suite_ws = os.path.join(SUITE_TEST_WORKSPACE_PATH, "suites")
    f = open(os.path.join(SUITE_TEST_WORKSPACE_PATH, "log.txt"), "w+")
    directory_loader = PluginDirectorySuiteLoader(suites_dir=suite_ws)

    def test_loading_test_suite(self):
        suite_dir = os.path.join(self.src_root, "DummyTestSuite")
        suite = self.directory_loader.load(suite_dir_path=suite_dir, f=self.f)
        assert len(suite) == 1
        assert suite[0].suite_name == "DummyTestSuite"

    def test_fail_load_due_to_missing_files(self):
        suite_dir = os.path.join(self.src_root, "MissingFiles")
        suite = self.directory_loader.load(suite_dir_path=suite_dir, f=self.f)
        assert len(suite) == 0

    def test_fail_load_invalid_path(self):
        suit_dir = "file-does-not-exist"
        suite = self.directory_loader.load(suit_dir, self.f)
        assert len(suite) == 0

    def test_load_hilab_suite(self):
        assert self.directory_loader.load(
            "/Users/yike/GailBot/gailbot_workspace/gailbot_data/plugin_source/suites/HiLabSuite/", self.f)

    def test_download_from_req_file(self):
        req = os.path.join(self.src_root, "req.txt")
        with open(req, "w+") as f:
            f.write("scrapy==2.11.1")
        lib_src = os.path.join(self.src_root, "req")
        os.mkdir(lib_src)
        assert self.directory_loader.download_packages(req, dest=lib_src)
        paths = paths_in_dir(lib_src)
        lib_exist = False
        for p in paths:
            if "scrapy" in get_name(p).lower():
                lib_exist = True
        delete(lib_src)
        assert lib_exist


if __name__ == '__main__':
    unittest.main()
