import xler8
import datetime
import sys


def dmaker_text(days_back=7):
    res = []
    start_day = datetime.datetime.now(tz=datetime.UTC)
    some_days = [ start_day - datetime.timedelta(days=x) for x in range(days_back) ]
    for dt in some_days:
        dts = dt.isoformat().split("T")[0]
        dows = dt.strftime(" %a ")
        if dt.isoweekday() >= 6:
            dows = "     "
        res.append(dts + dows)
    res.reverse()
    for line in res:
        print(line)


if len(sys.argv) > 1:
    dmaker_text(int(sys.argv[1]))
else:
    dmaker_text()
