#!/bin/sh

case "$1" in
	"i")
		idle=$(dbus-send --session --dest=org.freedesktop.ScreenSaver \
   			--type=method_call --print-reply=literal /ScreenSaver \
   			org.freedesktop.ScreenSaver.GetSessionIdleTime)
		echo $idle | cut -d " " -f 2
		;;
	"l")
		locked=$(dbus-send --session --dest=org.freedesktop.ScreenSaver \
   			--type=method_call --print-reply=literal /ScreenSaver \
  			org.freedesktop.ScreenSaver.GetActive)
		echo $locked | cut -d " " -f 2
		;;
	"a")
		wid=$(xprop -root 32x '\t$0' _NET_ACTIVE_WINDOW | cut -f 2)
		name=$(xprop -id $wid _NET_WM_NAME | cut -d '=' -f 2 | xargs)
		temp="${name%\"}"
		name="${temp#\"}"
		pid=$(xprop -id $wid _NET_WM_PID | cut -d '=' -f 2)
		process=$(ps axco pid,command | grep $pid | awk '{print $2}')
		echo $process, $name
		;;
esac