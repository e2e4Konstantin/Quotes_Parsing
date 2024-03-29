from .quote_definition import Resource, resource_data, TableItem, Header, resource_tables, HeaderOption, Attribute, \
    Option
from config.settings import SourceData
from .check_by_list import check_by_list
import re
from difflib import SequenceMatcher


def skip_empty_cells(data: SourceData, row, start_column) -> int:
    """ Пропускает пустые ячейки в строке row начиная с колонки start_column """
    for columns_i in range(start_column, data.column_max + 1):
        if data.get_cell_str_value(row, columns_i):
            return columns_i
    return data.column_max + 1


def get_attribute_table(data: SourceData, src_tables: TableItem, row: int, start_column: int) -> int:
    src_tables.attribute_table.clear()
    for column_i in range(start_column, data.column_max + 1):
        attribute_name = data.get_cell_str_value(row, column_i)
        if column_i > start_column and bool(data.get_cell_str_value(row - 1, column_i)):
            break
        if attribute_name:
            src_tables.attribute_table.append(Header(name_header=attribute_name, column_header=column_i))
    else:
        column_i = data.column_max + 1
    return column_i


def read_option_table(data: SourceData, src_tables: TableItem, row, start_column) -> int:
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


def get_options_tables(data: SourceData, src_tables: TableItem, row: int, start_column: int):
    src_tables.options_table.clear()
    column_i = skip_empty_cells(data, row, start_column)
    while column_i < data.column_max:
        column_i = read_option_table(data, src_tables, row, column_i)


def get_resource_table(data: SourceData, row: int, start_column: int):
    tmp_table = TableItem(row_table=row, number_table=str(len(resource_tables)))
    tmp_table.name_table = f"RES_{tmp_table.number_table}"
    tmp_table.cod_table = f"{tmp_table.number_table}.{row}"

    options_start_column = get_attribute_table(data, tmp_table, row, start_column)
    get_options_tables(data, tmp_table, row, options_start_column)

    resource_tables.append(tmp_table)


def read_tables_resource_old(data: SourceData):
    pattern_res_tab = re.compile(r"Атрибуты")
    column_number = data.get_column_number("H")

    for row in range(0, data.row_max + 1):
        value = data.get_cell_str_value(row, column_number)
        if pattern_res_tab.match(value):
            value_bottom_row = data.get_cell_str_value(row + 1, column_number)
            if value_bottom_row:
                get_resource_table(data, row + 1, column_number)


def read_tables_resource(data: SourceData):
    """
    Читает данные о таблице в которую сгруппированы ресурсы
    """
    bywords = ['Атрибуты', 'Астрибуты', 'Атибуты', 'Атрибут', 'Aтрибуты', 'Атрибуы', 'Aтрибуы', 'Арибуты']
    bywords = [x.lower() for x in bywords]
    column_number = data.get_column_number("J")

    for row in range(0, data.row_max + 1):
        value = data.get_cell_str_value(row, column_number)
        value = value.lower()
        # минимальная похожесть
        value_ratio = max([SequenceMatcher(None, value, ratio).ratio() for ratio in bywords])
        if value_ratio >= 0.85:
            # значение ячейки под словом 'Атрибуты'
            value_bottom_row = data.get_cell_str_value(row + 1, column_number)
            if value_bottom_row:
                get_resource_table(data, row + 1, column_number)


def is_data_on_right_side(data: SourceData, row: int, starting_column: str) -> bool:
    for column in range(data.get_column_number(starting_column), data.column_max + 1):
        if data.get_cell_str_value(row, column):
            return True
    return False


def get_resource(data: SourceData, row: int, parent_table_index: int) -> Resource:
    """ Читает ресурс из data на строке row. """
    a_value = data.get_cell_str_value(row, data.get_column_number("A"))
    statistics_value = data.get_cell_str_value(row, data.get_column_number("H"))
    resource_item = Resource(
        row=row + 1,
        a_column=int(a_value) if a_value.isdigit() else 0,
        origin=data.get_cell_str_value(row, data.get_column_number("C")),
        press_mark=data.get_cell_str_value(row, data.get_column_number("D")),
        title=data.get_cell_str_value(row, data.get_column_number("E")).capitalize(),
        measuring_unit=data.get_cell_str_value(row, data.get_column_number("F")),
        use_count=int(statistics_value) if statistics_value.isdigit() else 0,
        parameterization=bool(data.get_cell_str_value(row, data.get_column_number("I"))),
        table=parent_table_index
    )
    # print(f"\tдля ресурса в строке: {row} найдена таблица : {resource_tables[parent_table_index].cod_table}")
    # заполняем атрибуты
    table = resource_tables[parent_table_index]
    if len(table.attribute_table) > 0:
        for attribute in table.attribute_table:
            value = data.get_cell_str_value(row, attribute.column_header)
            if value:
                resource_item.attributes_resource.append(
                    Attribute(name_attribute=attribute.name_header, value_attribute=value)
                )
    # заполняем параметры
    if len(table.options_table) > 0:
        for option in table.options_table:
            # создаем экземпляр параметра
            tmp_options = Option()
            # имя параметра
            tmp_options.name_option = option.name_header_option
            # читаем значения параметра
            for header_option in option.option_headers:
                value = data.get_cell_str_value(row, header_option.column_header)
                tmp_options.value_option.append((header_option.name_header, value))
            # добавить параметр если есть хоть одно непустое значение
            if any([x[1] for x in tmp_options.value_option]):
                resource_item.options_resource.append(tmp_options)
    return resource_item


def find_row_parent_table(row: int, table_rows: list[int]) -> int:
    """ Вернет индекс таблицы в списке, которая самая ближняя сверху """
    distance = {i: row - table_rows[i] for i in range(len(table_rows)) if row - table_rows[i] > 0}
    min_dist = min(distance, key=lambda i: distance[i], default=-1)
    return min_dist if min_dist >= 0 else -1


def read_resources(data: SourceData):
    """ Читает ресурсы из данных data. Проверяет строку по шаблону для ресурса. Записывает ресурс. """
    read_tables_resource(data)

    if len(resource_tables) > 0:
        table_rows: list[int] = [x.row_table for x in resource_tables]
        table_rows.sort()
        print(f"\nПрочитано таблиц ресурсов: {len(resource_tables)}")  # , {table_rows}

        resource_with_data = 0
        resource_without_data = 0
        for row_i in range(0, data.row_max + 1):
            if check_by_list(data, row_i, ['B', 'C', 'D'], "resource"):
                resource_with_data += 1
                if is_data_on_right_side(data, row_i, "J"):
                    owner_table_row = find_row_parent_table(row_i, table_rows)
                    if owner_table_row >= 0:
                        resource_data.append(get_resource(data, row_i, owner_table_row))
                    else:
                        print(f"для ресурса на строке {row_i} не найдена таблица.")
                else:
                    resource_without_data += 1

        print(f"\nОбработано строк: {data.row_max}")
        print(f"Обработано ресурсов: {resource_with_data}")

        print(f"Записано ресурсов: {len(resource_data)}")
        print(f"Ресурсов без параметров/атрибутов: {resource_without_data}")
    else:
        print(f"В ресурсах не найдено ни одной таблицы с атрибутами/параметрами")
