#!/bin/sh

# Taken from regulus6633's answer on StackOverflow
# http://stackoverflow.com/a/17966890
# returns osx (and probably BSD) idle time in seconds 

echo $((`ioreg -c IOHIDSystem | sed -e '/HIDIdleTime/ !{ d' -e 't' -e '}' -e 's/.* = //g' -e 'q'` / 1000000000))