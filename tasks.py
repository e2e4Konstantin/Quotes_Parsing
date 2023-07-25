from utilites import (SourceData, tables, quotes, collections, failed_tables,
                      check_cod_quotes, read_collection, read_tables, read_quotes,
                      resource_data, read_resources,
                      read_equipment, equipment_data,
                      ExcelControl)
import contextlib
import io
import gc
import sys
import os
import pprint
import pickle


def save_all_to_excel_file(file_name: str, file_path: str, use_type: str, console_text: str = "") -> None:
    book_out = ExcelControl(file_name, file_path, use_type)
    with book_out as ex:
        ex.save_quotes(quotes)
        ex.save_attributes(quotes)
        ex.save_options(quotes)
        ex.save_collections(collections)
        ex.save_tables(tables)
        ex.save_failed_tables(failed_tables)
        ex.save_console(console_text)


def mill_quote_data_file(file_data: tuple[str, str, str]) -> None:
    print(f"файл: {file_data[0]}, лист: {file_data[2]}, папка: {file_data[1]}")
    data = SourceData(file_name=file_data[0], file_path=file_data[1], sheet_name=file_data[2])
    print(data.df.info(verbose=False, show_counts=False))
    print(f"непустых значений в столбце 'G': {data.df[data.df.columns[6]].count()}", "\n")
    check_cod_quotes(data)
    read_collection(data)
    read_tables(data)
    read_quotes(data)
    del data
    gc.collect()


def handling_quotes(file_data: tuple[str, str, str]):
    s = io.StringIO()
    with contextlib.redirect_stdout(s):
        mill_quote_data_file(file_data)
        print(f"{'-' * 40}>>")
        for quote in quotes:
            quote.options_control()
        print()
    print(s.getvalue())

    # for quote in quotes:
    #     if quote.cod_quote == '3.9-16-2':
    #         pprint.pprint(quote, width=200)
    #         r = quote.options_control()
    #         print(r)
    #         break
    file_out = file_data[0][:-5] + "_output.xlsx"
    save_all_to_excel_file(file_out, r'output', "Quote", s.getvalue())


def stream_handling_quotes(files: list[tuple[str, str, str]]):
    s = io.StringIO()
    with contextlib.redirect_stdout(s):
        for file in files:
            mill_quote_data_file(file)
            print()
        print(f"\n<<{'-' * 50}>>\nПрочитано расценок: {len(quotes)}\n")
        for quote in quotes:
            quote.options_control()
        print()
    print(s.getvalue())

    with open(r'output\out_string.pickle', 'wb') as handle:
        pickle.dump(s.getvalue(), handle, protocol=pickle.HIGHEST_PROTOCOL)

    save_all_to_excel_file("template_all_output.xlsx", r'output', "Quote", s.getvalue())


def fill_data_from_file(file_data: tuple[str, str, str]) -> SourceData | None:
    print(f"файл: {file_data[0]}, лист: {file_data[2]}, папка: {file_data[1]}")
    data = SourceData(file_name=file_data[0], file_path=file_data[1], sheet_name=file_data[2])
    if data:
        print(data.df.info(verbose=False, show_counts=False))
        print(data, "\n")
        return data
    return None


def handling_resource(file_data: tuple[str, str, str]):
    s = io.StringIO()
    with contextlib.redirect_stdout(s):
        print(f"<<-----  Ресурсы Start ----->>")
        data = fill_data_from_file(file_data)
        print(f"непустых значений в столбце 'G': {data.df[data.df.columns[6]].count()}")
        read_resources(data)
        print(f"<<-----  Ресурсы End  ----->>")
    print(s.getvalue())

    file_out = file_data[0][:-5] + "_output.xlsx"
    book_out = ExcelControl(file_out, r'output', "Resource")
    with book_out as ex:
        ex.save_resources(resource_data)
        ex.save_resources_attributes(resource_data)
        ex.save_resources_options(resource_data)
        ex.save_console(s.getvalue())


def equipment_handling(file_data: tuple[str, str, str]):
    s = io.StringIO()
    with contextlib.redirect_stdout(s):
        print(f"<<-----  Оборудование Start  ----->>")
        data = fill_data_from_file(file_data)
        read_equipment(data)
        print(f"<<-----  Оборудование End  ----->>")
    print(s.getvalue())

    file_out = file_data[0][:-5] + "_output.xlsx"
    book_out = ExcelControl(file_out, r'output', "Equipment")
    with book_out as ex:
        ex.save_equipment(equipment_data)
        ex.save_equipment_attributes(equipment_data)
        ex.save_equipment_options(equipment_data)
        ex.save_console(s.getvalue())
