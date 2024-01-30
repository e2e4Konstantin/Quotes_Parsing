import os
from icecream import ic

from tasks import handling_quotes, handling_resource, stream_handling_quotes, equipment_handling

from config import work_place

now = "office"  # office  # home
_, src_path, output_path = work_place(now)

source_files = (
    "Материалы_1.xlsx",
    "Машины_2_68.xlsx",
    "Расценки_3_68.xlsx",
    "Расценки_4_68.xlsx",
    "Расценки_5_67.xlsx",
    "Оборудование_13.xlsx",
)
files_path = tuple([os.path.join(src_path, data_file) for data_file in source_files])

if __name__ == "__main__":
    data = files_path[4]
    ic(data)
    handling_quotes(data, 'name')

    # print(file_queue)
    # stream_handling_quotes(file_queue)

    # #
    # # fn = 3
    # # handling_quotes((source_files[fn][0], paths[pl], source_files[fn][1]))
    #
    # fn = 2     # машины Глава 2
    # handling_resource((source_files[fn][0], paths[pl], source_files[fn][1]))
    #
    # # Глава 1 Материалы - !!!! вставить пустой столбец H после G, что бы "атрибуты были в столбце J
    # # Глава 13 Оборудование
    # # fn = 13   # 1    13
    # # equipment_handling((source_files[fn][0], paths[pl], source_files[fn][1]))
