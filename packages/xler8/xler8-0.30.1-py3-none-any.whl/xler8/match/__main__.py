import sys
import xler8
import json


infile = sys.argv[1]
print("-- %s --" % infile)

sheetnames = xler8.xlsx_sheetnames(filename=infile)
data = xler8.xlsx(filename=infile)[sheetnames[0]]

#print(json.dumps(data, indent=4))

x = xler8.sheet_match(data, 'what', ["this"], ['what', 'eva'])
#print(json.dumps(x, indent=4))
