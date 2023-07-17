from .excel_config import ExcelControl
from .quote_definition import tables, quotes, collections, failed_tables


def save_result_excel_file(file_name: str, path: str, console_text: str):
    book_out = ExcelControl(file_name, path)
    with book_out as ex:
        ex.save_quotes(quotes)
        ex.save_attributes(quotes)
        ex.save_options(quotes)
        ex.save_collections(collections)
        ex.save_tables(tables)
        ex.save_failed_tables(failed_tables)
        ex.save_console(console_text)
