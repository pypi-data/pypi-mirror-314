from abc import ABC, abstractmethod


class Notification(ABC):
    COMMON_NAME = "Notification"

    @abstractmethod
    def send(self, message):
        pass
