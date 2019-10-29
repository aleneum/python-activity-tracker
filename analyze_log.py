import datetime
import time
import sys

summary = []
current_title = None 
current_app = None
current_ts = None

def parse_line(line):
    arr = line.split(',', 2)
    ts = int(arr[0])
    app = arr[1].strip()
    title = arr[2].strip()
    return ts, app, title

with open("activity.log", "r") as f:
    current_ts, current_app, current_title = parse_line(f.readline())
    for l in f.readlines():
        ts, app, title = parse_line(l)
        if current_app != app or current_title != title:
            summary.append((current_ts, ts - current_ts, current_app, current_title))
            current_app = app
            current_title = title
            current_ts = ts

after = 0
before = int(time.time())
try:
    after = int(time.mktime(datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d").timetuple()))
    before = int(time.mktime(datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d").timetuple()))
except IndexError:
    if len(sys.argv) == 2:
        before = after + 60 * 60 * 24

for l in summary:
    if before > l[0] > after:
        s = datetime.datetime.fromtimestamp(l[0]).strftime('%Y-%m-%d %H:%M:%S')
        print(s, l[2], l[3])
