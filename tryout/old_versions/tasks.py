import contextlib
import io
import gc
import sys
import pickle
from icecream import ic
from pathlib import Path

from config import SourceData
from utilites import (tables, quotes, collections, failed_tables,
                      check_cod_quotes, read_collection, read_tables, read_quotes,
                      resource_data, read_resources,
                      read_equipment, equipment_data, equipment_tables, resource_tables,
                      ExcelControl)

def _save_all_to_excel_file(file_name: str, file_path: str, use_type: str, console_text: str = "") -> None:
    book_out = ExcelControl(file_name, file_path, use_type)
    with book_out as ex:
        ex.save_quotes(quotes)
        ex.save_attributes(quotes)
        ex.save_options(quotes)
        ex.save_collections(collections)
        ex.save_tables(tables)
        ex.save_failed_tables(failed_tables)
        ex.save_console(console_text)


def _mill_quote_data_file(file_data: str, sheet_name: str) -> None:
    """ Читает данные из файла с расценками в класс SourceData. """
    # message = f"файл: {file_data!r}"
    # ic(message)
    data = SourceData(full_file_name=file_data, sheet_name=sheet_name)

    print(data.df.info(verbose=False, show_counts=False))
    print(f"непустых значений в столбце 'G': {data.df[data.df.columns[6]].count()}", "\n")
    # check_cod_quotes(data)
    read_collection(data)
    read_tables(data)
    read_quotes(data)
    del data
    gc.collect()


def handling_quotes(file_data: str, sheet_name: str) -> None:
    """ Обработка файла с расценками. """
    _mill_quote_data_file(file_data, sheet_name)
    print(f"{'-' * 40}>>")
    for quote in quotes:
        # print(f"{quote}")
        try:
            quote.options_control()
        except Exception as err:
            print(f"{quote}\nошибка контроля расценки: {err}")
            sys.exit()
    print()
    file_out = Path(file_data).name[:-5] + "_output.xlsx"
    _save_all_to_excel_file(file_out, r'output', "Quote", "") # "" s.getvalue()


def stream_handling_quotes(files: list[tuple[str, str, str]]):
    s = io.StringIO()
    with contextlib.redirect_stdout(s):
        for file in files:
            _mill_quote_data_file(file)
            print()
        print(f"\n<<{'-' * 50}>>\nПрочитано расценок: {len(quotes)}\n")
        for quote in quotes:
            quote.options_control()
        print()
    print(s.getvalue())

    with open(r'output\out_string.pickle', 'wb') as handle:
        pickle.dump(s.getvalue(), handle, protocol=pickle.HIGHEST_PROTOCOL)

    _save_all_to_excel_file("template_all_output.xlsx", r'output', "Quote", s.getvalue())


def fill_data_from_file(file_data: tuple[str, str, str]) -> SourceData | None:
    print(f"файл: {file_data[0]}, лист: {file_data[2]}, папка: {file_data[1]}")
    data = SourceData(file_name=file_data[0], file_path=file_data[1], sheet_name=file_data[2])
    if data:
        print(data.df.info(verbose=False, show_counts=False))
        print(data, "\n")
        return data
    return None


def handling_resource(file_data: tuple[str, str, str]):
    # s = io.StringIO()
    # with contextlib.redirect_stdout(s):
    print(f"<<-----  Ресурсы Start ----->>")
    data = fill_data_from_file(file_data)
    print(f"непустых значений в столбце 'G': {data.df[data.df.columns[6]].count()}")

    read_resources(data)

    print(f"<<-----  Ресурсы End  ----->>")
    # print(s.getvalue())

    file_out = file_data[0][:-5] + "_output.xlsx"
    book_out = ExcelControl(file_out, r'output', "Resource")
    with book_out as ex:
        ex.save_resources(resource_data)
        ex.save_resources_attributes(resource_data)
        ex.save_resources_options(resource_data)
        ex.save_resources_tables(resource_tables)
        # ex.save_console(s.getvalue())


def equipment_handling(file_data: tuple[str, str, str]):
    # s = io.StringIO()
    # with contextlib.redirect_stdout(s):
    print(f"<<-----  Оборудование Start  ----->>")
    data = fill_data_from_file(file_data)
    read_equipment(data)
    print(f"<<-----  Оборудование End  ----->>")
    # print(s.getvalue())

    file_out = file_data[0][:-5] + "_output.xlsx"
    book_out = ExcelControl(file_out, r'output', "Equipment")
    with book_out as ex:
        ex.save_equipment(equipment_data)
        ex.save_equipment_attributes(equipment_data)
        ex.save_equipment_options(equipment_data)
        ex.save_equipment_tables(equipment_tables)
        # ex.save_console(s.getvalue())
