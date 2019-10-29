from subprocess import check_output, CalledProcessError
import Quartz  # pyobjc-framework-Quartz
from os.path import dirname
import logging
import pkg_resources

try:
    loc = pkg_resources.resource_filename(__name__, '../data/')
except NotImplementedError:  # thrown when package is a zip and not an egg folder (py2app)
    loc = './data/'

_LOGGER = logging.getLogger(__name__)

def get_app(title, identifier):
    if title in ['Electron'] or identifier in ['org.gnu.Emacs']:
        return identifier.split('.')[-1]
    else:
        return title

def run_script():
    res = None
    try:
        res = check_output(['osascript', loc + 'getActiveWindow.scpt'])
    except CalledProcessError as e:
        _LOGGER.error("CalledProcessError: %s", e.output)
    return res

class DarwinBackend:

    @staticmethod
    def getActiveWindow():
        result = run_script()
        if result:
            process, identifier, title = result.decode("utf-8")[:-1].split(', ', 2)
            return get_app(process, identifier), title
        else:
            return None, None

    @staticmethod
    def getIdleTime():
        idle = check_output(['sh', loc + 'getIdleTime.sh'])
        return int(idle[:-1])
        
    @staticmethod
    def isLocked():
        d = Quartz.CGSessionCopyCurrentDictionary()
        unlocked = (d and 
                    d.get("CGSSessionScreenIsLocked", 0) == 0 and 
                    d.get("kCGSSessionOnConsoleKey", 0) == 1)
        return not unlocked

    @staticmethod
    def open_text(file):
        check_output(['open', file])

# test scripts
if __name__ == '__main__':
    print(run_script())
