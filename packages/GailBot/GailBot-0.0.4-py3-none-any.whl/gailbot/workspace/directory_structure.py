import os
from dataclasses import dataclass

from gailbot.shared.utils.general import make_dir
from gailbot.workspace import WorkspaceManager


@dataclass
class TemporaryFolder:
    def __init__(self, name: str):
        self.root = os.path.join(WorkspaceManager.temporary_ws, name)
        self.data_copy = os.path.join(self.root, "data_copy")
        self.analysis_ws = os.path.join(self.root, "analysis_ws")
        self.transcribe_ws = os.path.join(self.root, "transcribe_ws")
        self.format_ws = os.path.join(self.root, "format_ws")
        for directory in [self.root, self.data_copy, self.analysis_ws, self.transcribe_ws, self.format_ws]:
            if not os.path.isdir(directory):
                make_dir(directory, overwrite=True)


@dataclass
class OutputFolder:
    GB_RESULT_SIGNATURE = ".gailbot"
    MERGED_FILE_NAME = "merged"
    MERGED_FILE = "merged.wav"

    def __init__(self, root):
        self.root = root
        self.raw = os.path.join(self.root, "Raw")
        self.analysis = os.path.join(self.root, "Analysis")
        self.transcribe = os.path.join(self.raw, "Transcript")
        self.media = os.path.join(self.raw, "Media")
        self.about = os.path.join(self.root, "About")
        for directory in [self.root, self.raw, self.analysis, self.transcribe, self.media, self.about]:
            make_dir(directory, overwrite=True)

    @staticmethod
    def get_transcribe_dir(root: str):
        return os.path.join(root, "Raw/Transcript")
