from .quote_definition import Header, HeaderOption, tables, TableItem, failed_tables
from config.settings import SourceData, TABLES_NUMBER_PATTERN, DEBUG_ON
from .check_by_list import check_by_list


def attributes_get(data: SourceData, src_tables: TableItem, row: int) -> int:
    """ Читает названия атрибутов начиная с колонки 'О' до тех пор пока сверху пусто"""
    src_tables.attribute_table.clear()  # очищаем список атрибутов
    column_a = data.get_column_number("O")  # получаем номер колонки "O"

    for column_i in range(column_a, data.column_max + 1):
        attribute_name = data.get_cell_str_value(row, column_i)
        if column_i > column_a and bool(data.get_cell_str_value(row - 1, column_i)):
            break
        if attribute_name:
            src_tables.attribute_table.append(Header(name_header=attribute_name, column_header=column_i))
    else:
        column_i = data.column_max + 1
    return column_i


def read_options(data: SourceData, src_tables: TableItem, row, start_column) -> int:
    """ Читает таблицу параметра в строке row начиная со start_column, пока не встретит
    непустую ячейку в верхней строке.
            - имя параметра в строке сверху
            - названия значений параметра.
        :return номер строки в которой закончилось чтение
    """
    ci = data.column_max + 1
    if start_column < data.column_max:
        option_name = data.get_cell_str_value(row - 1, start_column)  # имя параметра
        if option_name:
            tmp_option = HeaderOption(column_header_option=start_column, name_header_option=option_name)
            for ci in range(start_column, data.column_max + 1):
                if ci > start_column and bool(data.get_cell_str_value(row - 1, ci)):
                    break
                option_header = data.get_cell_str_value(row, ci)
                if option_header:
                    tmp_option.option_headers.append(Header(name_header=option_header, column_header=ci))
            src_tables.options_table.append(tmp_option)
        else:
            ci = data.column_max + 1
    return ci


def skip_empty_cells(data: SourceData, row, start_column) -> int:
    """ Пропускает пустые ячейки в строке row начиная с колонки start_column """
    for columns_i in range(start_column, data.column_max + 1):
        if data.get_cell_str_value(row, columns_i):
            return columns_i
    return data.column_max + 1


def options_get(data: SourceData, src_tables: TableItem, row, start_column):
    """ Читает заголовки параметров"""
    src_tables.options_table.clear()
    column_i = skip_empty_cells(data, row, start_column)
    while column_i < data.column_max:
        column_i = read_options(data, src_tables, row, column_i)
        # column_i += 1


def pop_in_table_data(data: SourceData, row):
    full_name = data.get_cell_str_value(row, data.get_column_number("H"))
    result = TABLES_NUMBER_PATTERN.search(full_name)
    tmp_table = TableItem(
        cod_table=data.get_cell_str_value(row, data.get_column_number("F")),
        number_table=full_name[result.span()[0]:result.span()[1]],
        name_table=full_name[result.span()[1]:].strip().capitalize(),
        row_table=row+1
    )
    for column_i in range(data.get_column_number("B"), data.get_column_number("F")):    # читаем дерево каталога
        tmp_table.catalog_table.append(data.get_cell_str_value(row, column_i))
    column_options_start = attributes_get(data, tmp_table, row)                         # читаем заголовки атрибутов
    options_get(data, tmp_table, row, column_options_start)                             # читаем заголовки параметров
    tables[tmp_table.cod_table] = tmp_table                                             # добавляем таблицу в словарь
    if DEBUG_ON: print(f"#{len(tables):4} {tmp_table}")


def read_tables(data: SourceData):
    right_format_tables = []
    # failed_tables = [] объявлен в quote_definition.py
    failed_tables_count = 0
    for row_i in range(1, data.row_max):
        base_test = check_by_list(data, row_i, ['B', 'C', 'G', 'H'], "table") # 'D', 'E', 'F',
        if base_test:
            value = data.get_cell_str_value(row_i, data.get_column_number("H"))
            advanced_test = check_by_list(data, row_i - 1, ['L', 'O'], "table")
            if advanced_test:
                right_format_tables.append((row_i, value[:50]))
                # print(f"таблица {value[:30]}...")
                pop_in_table_data(data, row_i)
            else:
                failed_tables.append((row_i, value))
                failed_tables_count += 1

    print(f"Прочитано таблиц: {len(right_format_tables) + len(failed_tables)}")
    print(f"\tправильных: {len(right_format_tables)}")
    print(f"\tкривых: {failed_tables_count}")


