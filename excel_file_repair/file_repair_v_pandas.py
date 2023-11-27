import os
import sys
import re
import pandas
from icecream import ic

path = r"F:\Kazak\GoogleDrive\NIAC\parameterisation"
file_name = r"m1_template_3_68.xlsx"
full_path = os.path.join(path, file_name)
ic(full_path)
sheet_name = "name"

df = pandas.read_excel(full_path, sheet_name=sheet_name, header=None, dtype="object")
if not df.empty:
    row_max = df.shape[0] - 1
    column_max = df.shape[1] - 1
    ic(row_max, column_max)
    column_f = 5
    column_h = 7
    for row_i in range(2, row_max):
        code = df.iat[row_i, column_f]
        code_bottom = df.iat[row_i+1, column_f]
        value = df.iat[row_i, column_h]
        title = "" if pandas.isna(value) else str(value)
        table_re = re.compile(r"Таблица \d+\.\d+-\d+\.")
        match_result = table_re.match(title)
        if match_result:
            ic(row_i, code, code_bottom, title)



else:
    ic("данные не прочитались")
