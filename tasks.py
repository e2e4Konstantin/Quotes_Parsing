import contextlib
import io
import gc
import sys
import pickle
from icecream import ic
from pathlib import Path
from files_features import output_message_exit

from config import SourceData, OUTPUT_FILE_PATH
from utilites import (tables, quotes, collections, failed_tables,
                      check_cod_quotes, read_collection, read_tables, read_quotes,
                      resource_data, read_machines,
                      read_materials_equipment, equipment_data, equipment_tables, resource_tables,
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


def _read_data_from_file(file_data: str, sheet_name: str, item_name: str) -> SourceData | None:
    data = SourceData(full_file_name=file_data, sheet_name=sheet_name, item_name=item_name)
    if data.df.empty:
        output_message_exit(f"не прочитаны данные из файла", f"{file_data!r} таблица: {sheet_name!r}")
        return None
    print(data)
    print(f"непустых значений в столбце 'G': {data.df[data.df.columns[6]].count()}")
    return data


def _mill_quote_data_file(file_data: str, sheet_name: str) -> None:
    """ Читает и обрабатывает данные из файла с расценками. """
    print(f"<<----- Расценки Start ----->>")
    data = _read_data_from_file(file_data, sheet_name, item_name="Quote")
    # check_cod_quotes(data)
    read_collection(data)
    read_tables(data)
    read_quotes(data)
    del data
    gc.collect()


def quotes_handling(file_data: str, sheet_name: str) -> None:
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
    _save_all_to_excel_file(file_out, r'output', "Quotes", "")  # "" s.getvalue()


def stream_quotes_handling(files: tuple[str, ...], sheet_name: str):
    """ Обработка списком. Запись в один файл."""
    for file in files:
        _mill_quote_data_file(file, sheet_name)
        print()
    print(f"\n<<{'-' * 50}>>\nПрочитано расценок: {len(quotes)}\n")
    for quote in quotes:
        quote.options_control()
    print()
    # with open(r'output\quotes_all.pickle', 'wb') as pickle_file:
    #     pickle.dump(quotes, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)
    _save_all_to_excel_file("Расценки_all_output.xlsx", r'output', "Quote", "")


def machines_handling(file_data: str, sheet_name: str):
    """ Читает и обрабатывает данные из файла с машинами, Глава 2. """
    print(f"<<-----  Машины Start ----->>")
    data = _read_data_from_file(file_data, sheet_name, "Machines")
    read_machines(data)
    print(f"<<-----  Машины End  ----->>")

    file_out = Path(file_data).name[:-5] + "_output.xlsx"
    book_out = ExcelControl(file_out, OUTPUT_FILE_PATH, "Machines")
    with book_out as ex:
        ex.save_resources(resource_data)
        ex.save_resources_attributes(resource_data)
        ex.save_resources_options(resource_data)
        ex.save_resources_tables(resource_tables)


def materials_equipment_handling(file_data: str, sheet_name: str, item_name: str):

    print(f"<<-----  {item_name!r} Start  ----->>")
    data = _read_data_from_file(file_data, sheet_name, item_name)
    read_materials_equipment(data)
    print(f"<<-----  {item_name!r} End  ----->>")

    file_out = Path(file_data).name[:-5] + "_output.xlsx"
    book_out = ExcelControl(file_out, OUTPUT_FILE_PATH, item_name)
    with book_out as ex:
        ex.save_equipment(equipment_data)
        ex.save_equipment_attributes(equipment_data)
        ex.save_equipment_options(equipment_data)
        ex.save_equipment_tables(equipment_tables)
