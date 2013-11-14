from subprocess import check_output, CalledProcessError
import Quartz
from os.path import dirname

loc = dirname(__file__)

def getActiveWindow():
    try:
        process, title = check_output(['osascript', loc + '/osx/getActiveWindow.scpt']).split(', ',1)
        return process, title
    except CalledProcessError as e:
        print "CalledProcessError"
        print e.output
    return None, None

def getIdleTime():
    idle = check_output(['sh', loc + '/osx/getIdleTime.sh'])
    return int(idle[:-1])
    
def isLocked():
    d = Quartz.CGSessionCopyCurrentDictionary()
    unlocked = (d and 
                d.get("CGSSessionScreenIsLocked", 0) == 0 and 
                d.get("kCGSSessionOnConsoleKey", 0) == 1)
    return not unlocked