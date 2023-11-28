from tasks import handling_quotes, handling_resource, stream_handling_quotes, equipment_handling

paths = {
    # "home": r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\1_targets\SRC\11-09-2023",
    "home": r"F:\Temp\NIAC",
    # "office": r"C:\Users\kazak.ke\Documents\Задачи\5_Fixed_Templates_07-09-2023",
    "office": r"\\bt7-doc\Exchange\Казак К.Э\от Велесь И.О\Файлы к переводу в машиночитаемый вид"
}

source_files = {
    0: (r"template_3_68_v_1.xlsx", "name"),
    3: (r"Расценки_3_68.xlsx", "name"),
    4: (r"template_4_68.xlsx", "name"),
    5: (r"quotes_5_67.xlsx", "name"),
    6: (r"quotes_6_68_25-10-2023.xlsx", "data"),

    7: (r"Статистика_1_13 Ресурсы.xlsx", "1"),      # Статистика_1_13 Ресурсы.xlsx / res_68.xlsx
    8: (r"Статистика_1_13 Оборудование.xlsx", "13"), #template_3_68_output.xlsx
    9: (r"renew_template_3_68_output.xlsx", "name"),

}
pl = "office"   #"home" # "office"

file_queue = [(source_files[x][0], paths[pl], source_files[x][1]) for x in list(source_files.keys())[1:4]]

#
if __name__ == "__main__":
    # print(file_queue)
    # stream_handling_quotes(file_queue)

    #
    fn = 3
    handling_quotes((source_files[fn][0], paths[pl], source_files[fn][1]))

    # fn = 6
    # handling_resource((source_files[fn][0], paths[pl], source_files[fn][1]))

    # fn = 7
    # equipment_handling((source_files[fn][0], paths[pl], source_files[fn][1]))
