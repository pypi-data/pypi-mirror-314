from abc import ABC, abstractmethod


class Watcher(ABC):
    @abstractmethod
    def watch(self, progress: str):
        pass
