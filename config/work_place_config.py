import os
from collections import namedtuple

PlacePath = namedtuple("PlacePath", ["db_file", "src_path", "output_path"])


def work_place(point_name: str) -> PlacePath:
    """ Формирует ссылки на данные в зависимости от места запуска. """
    db_name = "QuotesParsing.sqlite3"
    places = {
        "office": PlacePath(
            db_file=os.path.join(r"..\DB", db_name),
            src_path=r"\\bt7-doc\Exchange\Казак К.Э\от Велесь И.О\Файлы к переводу в машиночитаемый вид",
            output_path=r"..\output"
        ),
        "home": PlacePath(
            db_file=os.path.join(r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\production\Quotes_Parsing\DB", db_name),
            src_path=r"F:\Kazak\GoogleDrive\NIAC\Велесь_Игорь\Файлы к переводу в машиночитаемый вид\07-12-2023",
            output_path=r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\production\Quotes_Parsing\output"
        ),
    }
    return places[point_name]


if __name__ == '__main__':
    now = "home"  # office  # home
    # _, data, param = work_place(now)
    db, data, param = work_place(now)
    print(db,  data, param)
    print(work_place(now))
    print(work_place(now).db_file)



# paths = {
#     # "home": r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\1_targets\SRC\11-09-2023",
#     # "home": r"F:\Kazak\GoogleDrive\NIAC\parameterisati/on",
#     "home": r"F:\Kazak\GoogleDrive\NIAC\Велесь_Игорь\Файлы к переводу в машиночитаемый вид\07-12-2023",
#     # "home": r"F:\Temp\NIAC",
#
#
#
#     # "office": r"C:\Users\kazak.ke\Documents\Задачи\5_Fixed_Templates_07-09-2023",
#     "office": r"\\bt7-doc\Exchange\Казак К.Э\от Велесь И.О\Файлы к переводу в машиночитаемый вид"
# }