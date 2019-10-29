import threading
import logging
from time import time, sleep
import re

_LOGGER = logging.getLogger(__name__)

rules = {
    'Terminal': re.compile('^Terminal'),
    'Browser': re.compile('^(firefox|google chrome)'),
    'Editor': re.compile('^(vscode|pycharm|emacs|sublime text)'),
}

class ActivityRunner:

    DEFAULT_SLEEP_TIME = 10  # in seconds
    DEFAULT_THRESHOLD = DEFAULT_SLEEP_TIME * 20  # in seconds
    LOG_MEMORY_TRESHOLD = 50

    def __init__(self, backend, file_name, log_interval=None, idle_threshold=None):
        super(ActivityRunner, self).__init__()
        self.running = False
        self.log = []
        self.os = backend
        self.file_name = file_name
        self.sleep_time = log_interval if log_interval else self.DEFAULT_SLEEP_TIME
        self.idle_threshold = idle_threshold if idle_threshold else self.DEFAULT_THRESHOLD
        self.thread = None

    def start(self):
        if not self.thread or self.running is False:
            self.thread = threading.Thread(target=self.run)
            self.thread.start()        

    def run(self):
        _LOGGER.info("Start tracking")
        self.running = True
        while self.running:
            if self.os.isLocked() is False and self.os.getIdleTime() < self.idle_threshold:
                process, title = self.os.getActiveWindow()
                if process is not None:
                    category = ""
                    p_lower = process.lower()
                    for cat, rule in rules.items():
                        if rule.match(p_lower):
                            category = cat
                            break
                    entry = (int(time()), process, category, title.encode("unicode_escape").decode("utf-8"))
                    self.log.append(entry)
                    _LOGGER.debug("Logging: %s", entry)
                    if len(self.log) > self.LOG_MEMORY_TRESHOLD:
                        self.writeToFile()
                else:
                    _LOGGER.warn("Could not retrieve active process name, skipping entry")
            else:
                self.log.append((int(time()), '',  ''))
                _LOGGER.debug("idle or locked")
            current_sleep = 0
            while self.running and current_sleep < self.sleep_time:
                sleep(1)
                current_sleep += 1
        _LOGGER.info("Exit tracking loop.")
        self.writeToFile()

    def writeToFile(self):
        _LOGGER.info("Flush log to %s", self.file_name)
        with open(self.file_name, "a") as f:
            for l in self.log:
                print("{},\"{}\",\"{}\",\"{}\"".format(*l), file=f)
        self.log.clear()

    def stop(self):
        _LOGGER.info("Stopping")
        self.running = False
        self.thread.join()
        self.thread = None

    def show_log(self):
        self.os.show_log(self.file_name)
