import xler8
import sys
import csv
import copy
from openpyxl.utils import get_column_letter

infile = sys.argv[1]
colname = sys.argv[2]


hdrs = xler8.headers0(infile)
data = xler8.xlsx0(infile)
for i in range(len(data[colname])):
    print(data[colname][i])
