import sys
import xler8
import copy
import json

arg_in1 = sys.argv[1]

print("Trying to text output [%s]..." % (arg_in1))

in1 = xler8.xlsx(arg_in1)
in1_sheets = xler8.xlsx_sheetnames(arg_in1)
for sheetname in in1_sheets:
    print("sheet [%s]..." % sheetname)
    hdr = list(in1[sheetname].keys())

    with open("%s.%s.txt" % (arg_in1, sheetname), "w") as f:
        cols=[]

        f.write(str(hdr))
        f.write(json.dumps(in1[sheetname], indent=4))

print("Trying to text output [%s]...done" % (arg_in1))
