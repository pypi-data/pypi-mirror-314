import sys
import xler8
import copy


def diff_xlsx(in1_filename, in2_filename, out1_filename, compare_cols):
    in1 = xler8.xlsx(in1_filename)
    in1_sheets = xler8.xlsx_sheetnames(in1_filename)
    
    in2 = xler8.xlsx(in2_filename)
    in2_sheets = xler8.xlsx_sheetnames(in2_filename)
    
    sheet1 = in1_sheets[0]
    in1_hdr = list(in1[sheet1].keys())
    
    sheet2 = in2_sheets[0]
    in2_hdr = list(in1[sheet2].keys())

    compare_indices = []
    for col in compare_cols:
        compare_indices.append(in1_hdr.index(col))

    in1_rows = []
    in2_rows = []

    for r0 in range(0, len(in1[sheet1][in1_hdr[0]])):
        row = [ in1[sheet1][x][r0] for x in in1_hdr ]
        in1_rows.append(row)

    for r0 in range(0, len(in2[sheet2][in2_hdr[0]])):
        row = [ in2[sheet2][x][r0] for x in in2_hdr ]
        in2_rows.append(row)

    res_data = [in1_hdr]
    
    other = in2_rows
    for row in in1_rows:
        row_in_other = False
        for other_row in other:
            col_match_count = 0
            for col_index in compare_indices:
                if row[col_index] == other_row[col_index]:
                    col_match_count += 1
                
            if col_match_count == len(compare_indices):
                row_in_other=True
        
        if row_in_other == False:
            res_data.append(row)
    
    other = in1_rows
    for row in in2_rows:
        row_in_other = False
        for other_row in other:
            col_match_count = 0
            for col_index in compare_indices:
                if row[col_index] == other_row[col_index]:
                    col_match_count += 1
                
            if col_match_count == len(compare_indices):
                row_in_other=True

        if row_in_other == False:
            res_data.append(row)
    
    xler8.out(out1_filename, sheets={sheet1:{'data': res_data}})


arg_in1 = sys.argv[1]
arg_in2 = sys.argv[2]
arg_out1 = sys.argv[3]
arg_cols = sys.argv[4].split(",")

print("Trying to generate Diff [%s] <-> [%s] into [%s] based on comparing %d columns %s" % (arg_in1, arg_in2, arg_out1, len(arg_cols), str(arg_cols)))
diff_xlsx(arg_in1, arg_in2, arg_out1, arg_cols)
