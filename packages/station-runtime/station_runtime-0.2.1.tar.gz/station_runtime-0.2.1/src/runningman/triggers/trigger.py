import logging
from abc import abstractmethod
from typing import Optional
from threading import Thread, Event

from runningman.status import TriggerStatus, thread_status


class Trigger:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug(f"Init {self}")
        self.targets = []
        self.runner = None
        self.exit_event = Event()
        self.status = TriggerStatus.NotStarted

    @abstractmethod
    def run(self):
        pass

    def start(self):
        if self.status == TriggerStatus.Started:
            self.logger.debug("Already started")
            return
        self.logger.debug("Starting")
        self.exit_event.clear()
        self.runner = Thread(target=self.run)
        self.runner.start()
        self.status = TriggerStatus.Started

    def stop(self, timeout: Optional[float] = None):
        if self.status == TriggerStatus.Stopped:
            self.logger.debug("Already stopped")
            return
        self.logger.debug("Stopping")
        self.exit_event.set()
        self.runner.join(timeout)
        self.status = TriggerStatus.Stopped

    def get_status(self):
        return self.status, thread_status(self.runner)
