from .quote_definition import tables, quotes, Attribute, Quote, Option, heap, TableItem, collections
from .settings import SourceData, DEBUG_ON
from .check_by_list import check_by_list
import csv
from dataclasses import fields


def get_quote(data: SourceData, row: int, own_table: TableItem) -> Quote:
    """ Читает расценку из data на строке row в таблице own_table"""
    stat_val = data.get_cell_str_value(row, data.get_column_number("J"))
    unit_quote = Quote(
        row_quote=row+1,
        table_quote=data.get_cell_str_value(row, data.get_column_number("F")),
        cod_quote=data.get_cell_str_value(row, data.get_column_number("G")),
        name_quote=data.get_cell_str_value(row, data.get_column_number("H")).capitalize(),
        sizer_quote=data.get_cell_str_value(row, data.get_column_number("I")),
        statistics_quote=int(stat_val) if stat_val.isdigit() else 0,
        parameterized_quote=bool(data.get_cell_str_value(row, data.get_column_number("K"))),
        type_quote=data.get_cell_str_value(row, data.get_column_number("L")),
        parent_quote=data.get_cell_str_value(row, data.get_column_number("M"))
    )
    if own_table:
        # заполняем атрибуты
        if len(own_table.attribute_table) > 0:
            for attribute_i in own_table.attribute_table:
                value_i = data.get_cell_str_value(row, attribute_i.column_header)
                if value_i:
                    unit_quote.attributes_quote.append(
                        Attribute(name_attribute=attribute_i.name_header, value_attribute=value_i)
                    )
        # заполняем параметры
        if len(own_table.options_table) > 0:
            for option_i in own_table.options_table:
                # создаем экземпляр параметра
                tmp_options = Option()
                # имя параметра
                tmp_options.name_option = option_i.name_header_option
                # читаем значения параметра
                for header_option_i in option_i.option_headers:
                    value = data.get_cell_str_value(row, header_option_i.column_header)
                    tmp_options.value_option.append((header_option_i.name_header, value))
                # добавить параметр если есть хоть одно непустое значение
                if any([x[1] for x in tmp_options.value_option]):
                    unit_quote.options_quote.append(tmp_options)
        else:
            if DEBUG_ON: print(f"read_quote ->> {unit_quote.debug_str()}")
    return unit_quote


def get_collection(cod_table: str) -> str | None:
    """ Ищет код сборника таблице cod_table """
    if len(collections) > 0:
        for key in collections:
            if collections[key].cod in tables[cod_table].catalog_table:
                return key
    return None


def read_quotes(data: SourceData):
    """ Читает расценки из данных data.
        Проверяет строку по шаблону для расценки, ищет таблицу.
        Записывает расценку если у нее есть атрибуты или параметры.
        Расценки без параметров и атрибутов записывает в heap. """

    quotes_without_table = 0
    all_quotes = 0
    for row_i in range(0, data.row_max + 1):
        base_test = check_by_list(data, row_i, ['B', 'C', 'D', 'E', 'F', 'G'], "quote")
        if base_test:
            table_cod = data.get_cell_str_value(row_i, data.get_column_number("F"))
            all_quotes += 1
            own_table = tables.get(table_cod, None)
            if own_table:
                quote_i = get_quote(data, row_i, own_table)
                # ищем сборник для расценки
                key_collection = get_collection(quote_i.table_quote)
                if len(quote_i.attributes_quote) > 0 or len(quote_i.options_quote) > 0:
                    quotes.append(quote_i)
                    if key_collection:
                        collections[key_collection].quantity_parameterized_quotes += 1
                else:
                    heap.append(quote_i)
                    if key_collection:
                        collections[key_collection].quantity_not_parameterized_quotes += 1
                        collections[key_collection].not_parameterized_list.append(quote_i.cod_quote)

                    if DEBUG_ON: print(f"\t\tread_quotes >> Расценку {quote_i.cod_quote} "
                                       f"не запоминаем {len(quote_i.attributes_quote)} {len(quote_i.options_quote)}")
            else:
                quotes_without_table += 1
                if DEBUG_ON: print(
                    f"\tread_quotes ->> нет таблицы {table_cod} для расценки на строке {row_i+1}")

    print(f"\nПрочитано расценок: {all_quotes}")
    print(f"\tзаписано: {len(quotes)}")
    print(f"\tпустые атрибуты и параметры: {len(heap)}")
    qtable = len(quotes) + len(heap)
    print(f"\tвсего расценок в таблицах: {qtable}")
    print(f"\tбез таблиц: {all_quotes - qtable}")

    # if len(quotes) > 0:
    #     fp = r".\output\fine_quotes.txt"
    #     with open(fp, 'w', encoding='utf-8') as file_out:
    #         for i in range(len(quotes)):
    #             file_out.write(f"{i + 1:<5}: {quotes[i]}\n")  # .short_str()
    #
    #     column_name = [x.name for x in fields(quotes[0])]
    #     fp = r".\output\fine_quotes.csv"
    #     with open(fp, 'w', newline='') as file:
    #         writer = csv.writer(file, delimiter=';')  #
    #         writer.writerow(column_name)
    #         [writer.writerow(q.csv_list()) for q in quotes]
    #
    #
    # if len(heap) > 0:
    #     fp = r".\output\bug_quotes.txt"
    #     with open(fp, 'w', encoding='utf-8') as file_out:
    #         for i in range(len(heap)):
    #             file_out.write(f"{i + 1:<5}: {heap[i]}\n")  # .short_str()
    #
    #     column_name = [x.name for x in fields(heap[0])]
    #     fp = r".\output\bug_quotes.csv"
    #     with open(fp, 'w', newline='') as file:
    #         writer = csv.writer(file, delimiter=';')  #
    #         writer.writerow(column_name)
    #         [writer.writerow(q.csv_list()) for q in heap]

