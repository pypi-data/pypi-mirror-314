import xler8
import sys
import csv
import copy
from openpyxl.utils import get_column_letter
import rich
import rich.console
import rich.table

infile = sys.argv[1]

o_del = ","
o_del = ";"
o_quote = '"'

try:
    o_del = sys.argv[2]
    o_quote = sys.argv[3]
except:
    pass

C = rich.console.Console(width=8192)

t = rich.table.Table(title="file:%s:d=%s:q=%s" % (infile, o_del, o_quote), safe_box=True, padding=0)

hdrs=[]
data = []

with open(infile, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=o_del, quotechar=o_quote)

    h_mode=True
    for row in csvreader:
        if h_mode:
            h_mode = False
            hdrs = copy.deepcopy(row)
            continue

        row2 = [" >" + x + "< " for x in row]
        data.append(row2)

t.add_column("net-row-1", no_wrap=True)
for h in hdrs:
    t.add_column(h, no_wrap=True)

i=1
for row in data:
    row2 = [str(i)] + copy.deepcopy(row)
    t.add_row(*row2)
    i+=1

C.print(t)
