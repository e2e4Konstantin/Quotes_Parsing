from utilites import (SourceData, tables, quotes, collections, failed_tables,
                      check_cod_quotes, read_collection, read_tables, read_quotes,
                      resource_data, read_resources,
                      ExcelControl)
import contextlib
import io
import gc
import sys
import os
import pprint


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
    print(s.getvalue())
    file_out = file_data[0][:-5] + "_output.xlsx"
    save_all_to_excel_file(file_out, r'output', "Quote", s.getvalue())


def stream_handling_quotes(files: list[tuple[str, str, str]]):
    s = io.StringIO()
    with contextlib.redirect_stdout(s):
        for file in files:
            print(f"\n{file}")
            mill_quote_data_file(file)
        print(f"\n<<{'-' * 50}>>\nПрочитано расценок: {len(quotes)}")
    print(s.getvalue())

    save_all_to_excel_file("template_all_output.xlsx", r'output', "Quote", s.getvalue())


def handling_resource(file_data: tuple[str, str, str]):
    s = io.StringIO()
    with contextlib.redirect_stdout(s):
        data = SourceData(file_name=file_data[0], file_path=file_data[1], sheet_name=file_data[2])
        print(data, "\n")
        print(f"непустых значений в столбце 'G': {data.df[data.df.columns[6]].count()}", "\n")
        read_resources(data)
    print(s.getvalue())

    file_out = file_data[0][:-5] + "_output.xlsx"
    book_out = ExcelControl(file_out, r'output', "Resource")
    with book_out as ex:
        ex.save_resources(resource_data)
        ex.save_resources_attributes(resource_data)
        ex.save_resources_options(resource_data)
        ex.save_console(s.getvalue())
