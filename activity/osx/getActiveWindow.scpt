# taken from user Albert's answer on StackOverflow
# http://stackoverflow.com/questions/5292204/macosx-get-foremost-window-title
# tested on Mac OS X 10.7.5
 
global frontApp, frontAppName, windowTitle
 
set windowTitle to ""
tell application "System Events"
	set frontApp to first application process whose frontmost is true
	set frontAppName to name of frontApp
	tell process frontAppName
		try
			tell (1st window whose value of attribute "AXMain" is true)
				set windowTitle to value of attribute "AXTitle"
			end tell
		on error
			set windowTitle to frontAppName
		end try
	end tell
end tell
 
return {frontAppName, windowTitle}