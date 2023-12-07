from tasks import handling_quotes, handling_resource, stream_handling_quotes, equipment_handling

paths = {
    # "home": r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\1_targets\SRC\11-09-2023",
    # "home": r"F:\Kazak\GoogleDrive\NIAC\parameterisati/on",
    # "home": r"F:\Kazak\GoogleDrive\NIAC\Велесь_Игорь\Файлы к переводу в машиночитаемый вид\07-12-2023",
    "home": r"F:\Temp\NIAC",



    # "office": r"C:\Users\kazak.ke\Documents\Задачи\5_Fixed_Templates_07-09-2023",
    "office": r"\\bt7-doc\Exchange\Казак К.Э\от Велесь И.О\Файлы к переводу в машиночитаемый вид"
}

source_files = {
    1: (r"Материалы_1.xlsx", "report"),
    2: (r"Машины_2_68.xlsx", "data"),
    3: (r"Расценки_3_68.xlsx", "name"),
    4: (r"Расценки_4_68.xlsx", "name"),
    5: (r"Расценки_5_68.xlsx", "name"),
    6: (r"quotes_6_68_25-10-2023.xlsx", "data"),
    10: (r"Расценки_10_68.xlsx", "data"),

    13: (r"Оборудование_13.xlsx", "report"),

    33: (r"tmp_Расценки_4_68.xlsx", "name"),


}
pl = "home"   #"home" # "office"

file_queue = [(source_files[x][0], paths[pl], source_files[x][1]) for x in list(source_files.keys())[1:4]]

#
if __name__ == "__main__":
    # print(file_queue)
    # stream_handling_quotes(file_queue)

    #
    fn = 33
    handling_quotes((source_files[fn][0], paths[pl], source_files[fn][1]))

    # fn = 11     # машины Глава 2
    # handling_resource((source_files[fn][0], paths[pl], source_files[fn][1]))

    # Глава 1 Материалы - !!!! вставить пустой столбец H после G, что бы "атрибуты были в столбце J
    # Глава 13 Оборудование
    # fn = 13   # 1    13
    # equipment_handling((source_files[fn][0], paths[pl], source_files[fn][1]))
