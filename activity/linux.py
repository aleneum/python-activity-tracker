# Thank you chris for this nice post:
# http://thp.io/2007/09/x11-idle-time-and-focused-window-in.html

from subprocess import check_output, CalledProcessError
from os.path import dirname
import ctypes

info_script="dbusCommands.sh"
loc = dirname(__file__)+"/lnx/"+info_script

def getActiveWindow():
    try:
        process, title = check_output(['sh', loc, 'a'])[:-1].split(', ',1)
        return process, title
    except CalledProcessError as e:
        print "CalledProcessError"
        print e.output
    return None, None

def getIdleTime():
    time = check_output(['sh', loc, 'i'])[:-1]
    return int(time)/1000

def isLocked():
    state = check_output(['sh', loc, 'l'])[:-1]
    return state is "true"
