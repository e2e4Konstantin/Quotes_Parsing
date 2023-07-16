from utilites import SourceData, check_cod_quotes, read_collection, read_tables, read_quotes, save_result_excel_file
import contextlib
import io
import pprint

# fp = r"F:\Kazak\Google Диск\1_KK\Job_CNAC\office_targets\tasck_2\tmp2"
# fn = r"template_3_68_v_2.xlsx"
# fn = r"template_5_67_v_1.xlsx"
# sn = 'name'

fp = r"F:\Kazak\Google Диск\1_KK\Job_CNAC\office_targets\tasck_2\sources"
# fn = r"template_3_68.xlsx"
# fn = r"template_4_68.xlsx"
fn = r"template_5_67.xlsx"
sn = 'name'


s = io.StringIO()
with contextlib.redirect_stdout(s):
    data = SourceData(file_name=fn, file_path=fp, sheet_name=sn)
    print(data, "\n")
    print(f"непустых значений в столбце 'G': {data.df[data.df.columns[6]].count()}", "\n")
    check_cod_quotes(data)
    read_collection(data)
    read_tables(data)
    read_quotes(data)
print(s.getvalue())


fo = fn[:-5] + "_output.xlsx"
save_result_excel_file(fo, r'output', s.getvalue())
