# Thank you chris for this nice post:
# http://thp.io/2007/09/x11-idle-time-and-focused-window-in.html
# and Jim Paris for his answer on superuser:
# http://superuser.com/questions/382616/detecting-currently-active-window

from subprocess import check_output, CalledProcessError
from os.path import dirname
import ctypes
loc = dirname(__file__)

def getActiveWindow():
	try:
        process, title = check_output(['sh', loc + '/lnx/getActiveWindow.sh']).split(', ',1)
        return process, title
    except CalledProcessError as e:
        print "CalledProcessError"
        print e.output
    return None, None

def getIdleTime():
	print "not implemented yet"
	sys.exit(1)

def isLocked():
	print "not implemented yet"
	sys.exit(1)