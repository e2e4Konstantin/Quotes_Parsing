from .quote_definition import collections, Collection, quotes, tables
from .settings import SourceData, DEBUG_ON
from .check_by_list import check_by_list


def fill_in_collection_data(data: SourceData, row):
    collection = Collection(
        cod=data.get_cell_str_value(row, data.get_column_number("C")),
        name=data.get_cell_str_value(row, data.get_column_number("H")).capitalize(),
        row_start=row + 1,
    )
    collections[collection.cod] = collection
    if DEBUG_ON: print(f"#{len(collections):4} {collection}")


def read_collection(data: SourceData):
    for row in range(0, data.row_max):
        base_test = check_by_list(data, row, ['B', 'C', 'D', 'E', 'F', 'G', 'H'], "collection")
        if base_test:
            # print(f"сборник: {data.get_cell_str_value(row, data.get_column_number('H'))}")
            fill_in_collection_data(data, row)
    print(f"Прочитано сборников: {len(collections)}\n")

