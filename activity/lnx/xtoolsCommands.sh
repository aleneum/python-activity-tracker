#!/bin/sh

case "$1" in
	"i") xprintidle
		;;
	"l")
		lo=$(xscreensaver-command -time | cut -d " " -f 4)
		locked=false; [ "$lo" = "blanked" ] && locked=true;
		echo "$locked"
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