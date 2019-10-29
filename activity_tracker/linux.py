# Thank you chris for this nice post:
# http://thp.io/2007/09/x11-idle-time-and-focused-window-in.html

from subprocess import check_output, CalledProcessError
import pkg_resources

info_script="dbusCommands.sh"
loc = pkg_resources.resource_filename(__name__, '../scripts/')
script_path = loc+info_script

class LinuxBackend:

    @staticmethod
    def getActiveWindow():
        try:
            process, title = check_output(['sh', script_path, 'a'])[:-1].split(', ',1)
            return process, title
        except CalledProcessError as e:
            print("CalledProcessError: ", e.output)
        return None, None

    @staticmethod
    def getIdleTime():
        time = check_output(['sh', loc, 'i'])[:-1]
        return int(time)/1000

    @staticmethod
    def isLocked():
        state = check_output(['sh', loc, 'l'])[:-1]
        return state is "true"
