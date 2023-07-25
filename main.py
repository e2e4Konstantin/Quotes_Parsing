from tasks import handling_quotes, handling_resource, stream_handling_quotes, equipment_handling

paths = {
    "home": r"F:\Kazak\Google Диск\1_KK\Job_CNAC\office_targets\tasck_2\sources",
    "office": r"C:\Users\kazak.ke\Documents\Задачи\Задача_2_exel_pars\данные\source",
}

source_files = {
    0: (r"template_3_68_v_1.xlsx", "name"),
    3: (r"template_3_68.xlsx", "name"),
    4: (r"template_4_68.xlsx", "name"),
    5: (r"template_5_67.xlsx", "name"),
    6: (r"Статистика_1_13 Ресурсы.xlsx", "1"), # Статистика_1_13 Ресурсы.xlsx / res_68.xlsx
    7: (r"Статистика_1_13 Оборудование.xlsx", "13"),

}
pl = "office"   #"home" # "office"

file_queue = [(source_files[x][0], paths[pl], source_files[x][1]) for x in list(source_files.keys())[1:4]]
#
if __name__ == "__main__":
    # stream_handling_quotes(file_queue)


    # fn = 5
    # handling_quotes((source_files[fn][0], paths[pl], source_files[fn][1]))

    fn = 6
    handling_resource((source_files[fn][0], paths[pl], source_files[fn][1]))

    # fn = 7
    # equipment_handling((source_files[fn][0], paths[pl], source_files[fn][1]))
