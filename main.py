import os
from icecream import ic

from tasks import machines_handling, quotes_handling, stream_quotes_handling, materials_equipment_handling

from config import work_place

now = "office"  # office  # home
_, src_path, output_path = work_place(now)

source_files = (
    "Расценки_3_68.xlsx",
    "Расценки_4_68.xlsx",
    "Расценки_12_67.xlsx",
    "Расценки_10_68.xlsx",
    "Материалы_1.xlsx",
    "Машины_2_68.xlsx",
    "Оборудование_13.xlsx",
)
files_path = tuple([os.path.join(src_path, data_file) for data_file in source_files])

if __name__ == "__main__":
    data = files_path[1]
    ic(data)
    quotes_handling(data, 'name')

    # for data in files_path[:4]:
    #     ic(data)
    #     quotes_handling(data, sheet_name='name')

    # print(files_path[:4])
    # stream_quotes_handling(files_path[:4], sheet_name='name')

    # # машины Глава 2
    # data = files_path[5]
    # ic(data)
    # machines_handling(data, 'data')

    # # Материалы Глава 1
    # # !!!! вставить пустой столбец H после G, что бы "атрибуты были в столбце J
    # data = files_path[4]
    # ic(data)
    # materials_equipment_handling(data, sheet_name='data', item_name='Materials')

    # # Оборудование Глава 13
    # # !!!! вставить пустой столбец H после G, что бы "атрибуты были в столбце J
    # data = files_path[6]
    # ic(data)
    # materials_equipment_handling(data, sheet_name='data', item_name='Equipment')
