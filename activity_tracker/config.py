import json
from os.path import exists, expanduser
from shutil import copyfile
import pkg_resources
import re

try:
    loc = pkg_resources.resource_filename(__name__, '../data/')
except NotImplementedError:  # thrown when package is a zip and not an egg folder (py2app)
    loc = './data/'

class Config:

    def __init__(self, config_path):
        if not exists(config_path):
            copyfile(loc + 'default_config.json', config_path)
        with open(config_path, 'r') as fp:
            self.data = json.load(fp)
        self.rules = {}
        for cat, rule in self.data['rules'].items():
            self.rules[cat] = re.compile(rule.lower())

    @property
    def log_interval(self):
        return self.data['log_interval']

    @property
    def log_path(self):
        return expanduser(self.data['log_path'])

    @property
    def idle_threshold(self):
        return self.data['idle_threshold']

    @property
    def memory_limit(self):
        return self.data['memory_limit']

    @property
    def debug_path(self):
        return expanduser(self.data['debug_path']) if 'debug_path' in self.data else None


if __name__ == '__main__':
    conf = Config(expanduser('~/.config/activity_tracker.json'))
    print(conf.rules)
