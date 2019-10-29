import threading
import logging
from time import time, sleep
import re

from activity_tracker.config import Config

_LOGGER = logging.getLogger(__name__)

class ActivityRunner:

    def __init__(self, backend, config):
        super(ActivityRunner, self).__init__()
        self.running = False
        self.log = []
        self.os = backend
        self.config_path = config
        self.config = Config(config)
        self.thread = None

    def start(self):
        if not self.thread or self.running is False:
            self.thread = threading.Thread(target=self.run)
            self.thread.start()        

    def run(self):
        _LOGGER.info("Start tracking")
        self.running = True
        while self.running:
            if self.os.isLocked() is False and self.os.getIdleTime() < self.config.idle_threshold:
                process, title = self.os.getActiveWindow()
                if process is not None:
                    category = ""
                    p_lower = process.lower()
                    for cat, rule in self.config.rules.items():
                        if rule.match(p_lower):
                            category = cat
                            break
                    entry = (int(time()), process, category, title.encode("unicode_escape").decode("utf-8"))
                    self.log.append(entry)
                    _LOGGER.debug("Logging: %s", entry)
                    if len(self.log) > self.config.memory_limit:
                        self.writeToFile()
                else:
                    _LOGGER.warn("Could not retrieve active process name, skipping entry")
            else:
                self.log.append((int(time()), '',  ''))
                _LOGGER.debug("idle or locked")
            current_sleep = 0
            while self.running and current_sleep < self.config.log_interval:
                sleep(1)
                current_sleep += 1
        _LOGGER.info("Exit tracking loop.")
        self.writeToFile()

    def writeToFile(self):
        _LOGGER.info("Flush log to %s", self.config.log_path)
        with open(self.config.log_path, "a") as f:
            for l in self.log:
                print("{},\"{}\",\"{}\",\"{}\"".format(*l), file=f)
        self.log.clear()

    def stop(self):
        _LOGGER.info("Stopping")
        self.running = False
        self.thread.join()
        self.thread = None

    def show_log(self):
        self.os.open_text(self.config.log_path)

    def show_config(self):
        self.os.open_text(self.config_path)
