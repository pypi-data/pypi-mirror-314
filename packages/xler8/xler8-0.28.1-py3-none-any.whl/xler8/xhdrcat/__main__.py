import xler8
import sys
import csv
import copy
from openpyxl.utils import get_column_letter

infile = sys.argv[1]

hdrs = xler8.headers0(infile)
for h in hdrs:
    print(h)
