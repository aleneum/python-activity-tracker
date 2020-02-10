from subprocess import check_output, CalledProcessError, Popen, PIPE
from os.path import dirname
from os import environ
import logging
import pkg_resources

try:
    loc = pkg_resources.resource_filename(__name__, '../data/')
except NotImplementedError:  # thrown when package is a zip and not an egg folder (py2app)
    loc = './data/'

_LOGGER = logging.getLogger(__name__)

def run_script(ps_file):
    res = None
    try:
        cmd =  [f"{environ['windir']}\\System32\\WindowsPowerShell\\v1.0\\powershell.exe", "-ExecutionPolicy", "Bypass", 
                "-File", loc + ps_file]
        res = check_output(cmd).decode("utf-8")[:-2]
    except CalledProcessError as e:
        _LOGGER.error("CalledProcessError: %s", e.output)
    return res


class WindowsBackend:

    @staticmethod
    def getActiveWindow():
        result = run_script('getActiveWindow.ps1')
        if result is not None:
            name, description, title = result.split(', ', 2) # name is process name, description usually more readable
            return name, description, title
        else:
            return None, None

    @staticmethod
    def getIdleTime():
        res = run_script("getIdleTime.ps1")
        return float(res) if res else 0

    @staticmethod
    def isLocked():
        return "LogonUI.exe" in str(check_output("TASKLIST"))

    @staticmethod
    def open_text(file_path):
        check_output(['start', file_path], shell=True)


if __name__ == '__main__':
    import time
    time.sleep(1)
    print(float(run_script("getIdleTime.ps1")))
    print(run_script("getActiveWindow.ps1"))