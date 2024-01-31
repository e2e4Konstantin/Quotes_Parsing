from .quote_definition import TableItem, Header, HeaderOption, Attribute, Option
from .quote_definition import Equipment, equipment_data, equipment_tables

from config.settings import SourceData
from .check_by_list import check_by_list, skip_empty_cells
import re


def get_attribute_table(data: SourceData, src_tables: TableItem, row: int, start_column: int) -> int:
    """ Читает таблицу атрибутов """
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
    """ Читает таблицу для параметра """
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
    """ Читает таблицы для всех параметров """
    src_tables.options_table.clear()
    column_i = skip_empty_cells(data, row, start_column)
    while column_i < data.column_max:
        column_i = read_option_table(data, src_tables, row, column_i)


def get_equipment_table(data: SourceData, row: int, start_column: int):
    """ Читает таблицу в строке row"""
    tmp_table = TableItem(row_table=row, number_table=str(len(equipment_tables)))
    tmp_table.name_table = f"EQP_{tmp_table.number_table}"
    tmp_table.cod_table = f"{tmp_table.number_table}.{row}"

    options_start_column = get_attribute_table(data, tmp_table, row, start_column)
    get_options_tables(data, tmp_table, row, options_start_column)

    equipment_tables.append(tmp_table)


def read_tables_equipment(data: SourceData):
    """ Читает все таблицы в data для элементов оборудования по признаку:
     значение в столбце I, соответствует паттерну pattern_eqp_tab.  """

    pattern_eqp_tab = re.compile(r"атрибуты")
    column_number = data.get_column_number("I")

    for row in range(0, data.row_max + 1):
        value = data.get_cell_str_value(row, column_number)
        if value and pattern_eqp_tab.match(value.lower()):
            value_bottom_row = data.get_cell_str_value(row + 1, column_number)
            if value_bottom_row:
                get_equipment_table(data, row + 1, column_number)


def is_data_on_right_side(data: SourceData, row: int, starting_column: str) -> bool:
    """ Проверяет есть ли данные справа от ячейки (row, starting_column). """
    for column in range(data.get_column_number(starting_column), data.column_max + 1):
        if data.get_cell_str_value(row, column):
            return True
    return False


def get_device(data: SourceData, row: int, parent_table_index: int) -> Equipment:
    """ Читает строку с устройством из data на строке row. """
    a_value = data.get_cell_str_value(row, data.get_column_number("A"))
    statistics_value = data.get_cell_str_value(row, data.get_column_number("F"))
    equipment_item = Equipment(
        row=row + 1,
        a_column=int(a_value) if a_value.isdigit() else 0,
        origin=data.get_cell_str_value(row, data.get_column_number("B")),
        press_mark=data.get_cell_str_value(row, data.get_column_number("C")),
        title=data.get_cell_str_value(row, data.get_column_number("D")).capitalize(),
        measuring_unit=data.get_cell_str_value(row, data.get_column_number("E")),
        use_count=int(statistics_value) if statistics_value.isdigit() else 0,
        parameterization=bool(data.get_cell_str_value(row, data.get_column_number("G"))),
        remark=data.get_cell_str_value(row, data.get_column_number("H")),
        table=parent_table_index
    )
    # print(f"\tдля устройства в строке: {row} найдена таблица : {equipment_tables[parent_table_index].cod_table}")
    # заполняем атрибуты
    table = equipment_tables[parent_table_index]
    if len(table.attribute_table) > 0:
        for attribute in table.attribute_table:
            value = data.get_cell_str_value(row, attribute.column_header)
            if value:
                equipment_item.attributes_equipment.append(
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
                equipment_item.options_equipment.append(tmp_options)
    return equipment_item


def find_row_parent_table(row: int, table_rows: list[int]) -> int:
    """ Вернет индекс таблицы в списке table_rows, которая самая ближняя сверху от строки row. """
    distance = {i: row - table_rows[i] for i in range(len(table_rows)) if row - table_rows[i] > 0}
    min_dist = min(distance, key=lambda i: distance[i], default=-1)
    return min_dist if min_dist >= 0 else -1


def read_materials_equipment(data: SourceData):
    """ Читает строки с описанием оборудования/материала из данных data.
    Записывает элемент оборудования в список equipment_data. """

    read_tables_equipment(data)
    if len(equipment_tables) > 0:
        table_rows: list[int] = [x.row_table for x in equipment_tables]
        table_rows.sort()
        print(f"\nПрочитано таблиц {data.item_name!r}: {len(equipment_tables)}")

        equipment_with_data = 0
        equipment_without_data = 0
        for row_i in range(0, data.row_max + 1):
            if check_by_list(data, row_i, ['B', 'C', 'D'], "equipment"):
                equipment_with_data += 1
                if is_data_on_right_side(data, row_i, "H"):
                    owner_table_row = find_row_parent_table(row_i, table_rows)  # найти ближайшую сверху таблицу
                    if owner_table_row >= 0:
                        equipment_data.append(get_device(data, row_i, owner_table_row))
                    else:
                        print(f"для {data.item_name!r} на строке {row_i} не найдена таблица.")
                else:
                    equipment_without_data += 1

        print(f"\nОбработано строк: {data.row_max}")
        print(f"Обработано {data.item_name!r}: {equipment_with_data}")

        print(f"Записано {data.item_name!r}: {len(equipment_data)}")
        print(f"{data.item_name!r} без параметров/атрибутов: {equipment_without_data}")
    else:
        print(f"для {data.item_name!r} в фале {data.full_path}\nне найдено ни одной таблицы с атрибутами/параметрами")
