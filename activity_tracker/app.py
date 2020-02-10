import sys
import signal
import logging
from os.path import exists, expanduser

from activity_tracker.runner import ActivityRunner

_LOGGER = logging.getLogger(__name__)

if sys.platform == 'linux2':
    from activity_tracker.linux import LinuxBackend as Backend
    class App:
        @staticmethod
        def run(runner):
            signal.signal(signal.SIGTERM, runner.stop)
            signal.signal(signal.SIGQUIT, runner.stop)
            signal.signal(signal.SIGINT, runner.stop)
            runner.start()
            print("Ctrl+C or SIGTERM to close application")

elif sys.platform == 'darwin':
    from activity_tracker.darwin import DarwinBackend as Backend
    from activity_tracker.osx.toolbar import ToolbarApp as App
elif sys.platform == 'win32':
    from activity_tracker.windows import WindowsBackend as Backend
    from activity_tracker.win.toolbar import ToolbarApp as App
else:
    print("OS %s not supported yet" % sys.platform)
    sys.exit(1)

def main(argv=None):
    argv = argv if argv else sys.argv[1:]
    conf_file = expanduser('~/.config/activity_tracker.json')
    runner = ActivityRunner(backend=Backend, config=conf_file)
    App().run(runner)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main(sys.argv[1:])
