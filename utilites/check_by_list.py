from .settings import SourceData, DEBUG_ON


def check_by_list(data: SourceData, row: int, columns_list, item_name: str):
    """ Проверить строку по списку правил ['B', 'C', 'D'], 'equipment' """
    sign_luck = set()
    for column_name in columns_list:
        column_number = data.get_column_number(column_name)
        value_i = data.get_cell_str_value(row, column_number)

        template = data.test_templates[item_name][column_name]  # tuple (re.compile(r"^\s*$"), STRONG_MATCH)
        if template[1]:
            match_result = template[0].fullmatch(value_i)
        else:
            match_result = template[0].match(value_i)

        sign_luck.add(True) if match_result else sign_luck.add(False)

    if len(sign_luck) > 0:
        return not (False in sign_luck)
    return False


def skip_empty_cells(data: SourceData, row: int, start_column: int) -> int:
    """ Пропускает пустые ячейки в строке row начиная с колонки start_column.
        Возвращает номер первой непустой колонки или границу (максимальную колонку).
    """
    for columns_i in range(start_column, data.column_max + 1):
        if data.get_cell_str_value(row, columns_i):
            return columns_i
    return data.column_max + 1
