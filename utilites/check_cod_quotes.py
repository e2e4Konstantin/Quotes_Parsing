from .settings import SourceData, DEBUG_ON
from .check_by_list import check_by_list
import re

def check_cod_quotes(data: SourceData):
    template_g = re.compile(r"\d+\.\d+(-\d+)+")
    for row in range(0, data.row_max+1):
        base_test = check_by_list(data, row, ['B', 'C', 'D', 'E', 'F'], "quote")
        if base_test:
            column_number = data.get_column_number('G')
            value = data.get_cell_str_value(row, column_number)
            if value:
                match_result = template_g.match(value)
                if match_result.start() > 0 or match_result.end() < len(value):
                    # bad cod
                    print(f"\t!!! кривой номер расценки: '{value}' в строке: {row+1}")
