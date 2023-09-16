from abc import ABC, abstractmethod


class Bot(ABC):
    @abstractmethod
    def move(self) -> None:
        pass
