from abc import ABC, abstractmethod


class DB(ABC):
    def __init__(self) -> None:
        self._open()

        super().__init__()

    def __del__(self) -> None:
        self._close()

    @abstractmethod
    def _open(self) -> None:
        pass

    @abstractmethod
    def _close(self) -> None:
        pass
