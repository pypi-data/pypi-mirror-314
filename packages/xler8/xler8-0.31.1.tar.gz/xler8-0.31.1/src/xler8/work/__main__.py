import xler8
import datetime
import sys


def work_overview(filename, daymins=480):
    lines = []
    with open(filename, 'r') as f:
        lines = [ x.strip().split(" ") for x in f.read().strip().split("\n") if x.strip() != ""]
    
    alltags = {}
    alldays = {}

    for linecols in lines:
        dt = linecols[0] # date
        tg = linecols[1] # tag
        tm = int(linecols[2]) # tag minutes
        alltags[tg]=True
        alldays[dt]=True

    alltags = list(sorted(alltags.keys()))
    alldays = list(sorted(alldays.keys()))
    start_day_s = alldays[0]
    latest_day_s = alldays[-1]

    start_day = datetime.datetime.fromisoformat(start_day_s + "T00:00:00+00:00")
    latest_day = datetime.datetime.fromisoformat(latest_day_s + "T00:00:00+00:00")
    data_days = int((latest_day-start_day).days)

    some_days = [ start_day + datetime.timedelta(days=x) for x in range(data_days+1) ]

    data_ = {}
    for dt in some_days:
        dts = dt.isoformat().split("T")[0]
        minutes_value = (-1)*daymins
        if dt.isoweekday() >= 6:
            minutes_value = 0
        data_[dts] = { 'date': dts, 'minutes': minutes_value, 'acc': [0 for x in range(len(alltags))]}


    # accumulate data_ with logged minutes
    for linecols in lines:
        dt = linecols[0] # date
        tg = linecols[1] # tag
        tm = int(linecols[2]) # tag minutes
        o = data_[dt]
        tag_idx = alltags.index(tg)
        o['minutes'] += tm
        o['acc'][tag_idx] += tm


    data = [["day-of-week", "date", "day-miss"] + alltags]

    for d_ in some_days:
        d=d_.isoformat().split("T")[0]
        wota = d_.strftime("%a")
        if d_.isoweekday() >= 6:
            wota = ""
        if d in data_.keys():
            data.append([wota, d, data_[d]['minutes']]+data_[d]['acc'])
        else:
            data.append([wota, d])

    xler8.xlsx_out("%s.xlsx" % filename, sheets={
        "work":{
            'data': data,
            'cw': xler8.cw_gen(data, 2)
        }
    })

    print(start_day_s)
    print(latest_day_s)
    print((latest_day-start_day).days)


work_overview(sys.argv[1])
