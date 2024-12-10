import xler8
import sys
import csv
import copy
from openpyxl.utils import get_column_letter
import rich
import rich.console
import rich.table

infile = sys.argv[1]

C = rich.console.Console(width=8192)

t = rich.table.Table(title="file:%s" % (infile), safe_box=True, padding=0)


hdrs = xler8.headers0(infile)
data_ = xler8.xlsx0(infile)

t.add_column("net-row-1", no_wrap=True)
for h in hdrs:
    t.add_column(h, no_wrap=True)

for i in range(len(data_[hdrs[0]])):
    row2 = [str(i+1)] + [ " >"+str(x)+"< :%s " % type(x).__name__ for x in [data_[y][i] for y in hdrs]]
    t.add_row(*row2)

C.print(t)
