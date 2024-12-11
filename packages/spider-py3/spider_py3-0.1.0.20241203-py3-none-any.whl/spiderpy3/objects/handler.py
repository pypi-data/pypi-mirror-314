from abc import abstractmethod
from typing import Any

from spiderpy3.objects.task import Task


class Handler(Task):

    @abstractmethod
    def action(self, *args, **kwargs) -> Any:
        pass
