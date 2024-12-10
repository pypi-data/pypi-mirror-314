import os.path
import unittest

from gailbot.workspace import WorkspaceManager


class TestWorkspaceManager(unittest.TestCase):
    def test_init_workspace(self):
        ws = WorkspaceManager()
        ws.init_workspace()
        assert os.path.getctime(WorkspaceManager.gb_root) >= WorkspaceManager._last_update
        for p in WorkspaceManager.paths:
            assert os.path.isdir(p)

    def test_reset_workspace(self):
        ws = WorkspaceManager()
        ws.init_workspace()
        for p in WorkspaceManager.paths:
            assert os.path.isdir(p)
        orig_ws_creation_time = os.path.getctime(WorkspaceManager.gb_root)
        ws.reset_workspace()
        for p in WorkspaceManager.paths:
            assert os.path.isdir(p)
        reset_ws_creation_time = os.path.getctime(WorkspaceManager.gb_root)
        assert orig_ws_creation_time != reset_ws_creation_time


if __name__ == '__main__':
    unittest.main()
