import xler8
import argparse
import copy
from pprint import pprint as PP

parser = argparse.ArgumentParser()
parser.add_argument("-i", nargs=1, type=str, metavar="XLSX-INPUT", help="")
parser.add_argument("-t", nargs=1, type=str, action="append", metavar="COLUMN-TITLE", help="")
parser.add_argument("-f", nargs=1, type=str, action="append", metavar="CONTENT-TEXT-FILE", help="")
parser.add_argument("-o", nargs=1, type=str, metavar="VBA-OUTPUT-FILE", help="")


args = parser.parse_args()

match_values = {}

for i in range(len(args.t)):
    content = None
    with open(args.f[i][0], 'r') as f:
        content = f.read().strip().split("\n")
    match_values[args.t[i][0]] = copy.deepcopy(content)


data = xler8.xlsx0(args.i[0])
data_headers = xler8.headers0(args.i[0])

all_the_reasons = {}


for row in range(len(data[data_headers[0]])):
    # row=0 => BCDEF....:2 !!!
    kill_row_index = row+2
    for h in match_values.keys():
        if data[h][row] in match_values[h]:
            textual_kill = "%08d" % kill_row_index
            if not textual_kill in all_the_reasons.keys():
                all_the_reasons[textual_kill] = []
            all_the_reasons[textual_kill].append("column %s matches %s" % (h, data[h][row]))

# padded row indice
ordered = list(reversed(list(sorted(all_the_reasons.keys()))))

with open(args.o[0], 'w') as f:
    f.write("' auto generated xler8.vba row-killer\n");
    f.write("\n");
    f.write("Sub ReverseRowKiller()\n");
    f.write("  With Sheet1\n");
    for row_ in ordered:
        row = int(row_)
        f.write("    .Rows(%d).EntireRow.Delete\n" % row);
    f.write("  End With\n");
    f.write("End Sub\n");
    f.write("\n");


report_data = [['Row Number', 'Reasons', 'Number of Reasons']]

for row_ in reversed(ordered):
    row = int(row_)
    reasons = ", ".join(all_the_reasons[row_])
    report_data.append([str(row), reasons, str(len(all_the_reasons[row_]))])


filename_report = args.i[0] + "-row-kill-report.xlsx"
xler8.xlsx_out(filename=filename_report, sheets={
    "Reasons": {
        'data': report_data,
        'cw': xler8.cw_gen(report_data)
    }
})