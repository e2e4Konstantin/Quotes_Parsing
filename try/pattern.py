import re
STRONG_MATCH = True
SOFT_MATCH = False

pattern_common_bc = {
    "B": (re.compile(r"\d+"), STRONG_MATCH),  # 3
    "C": (re.compile(r"\d+\.\d+"), STRONG_MATCH),  # 3.6
}

pattern_common_def = {
    "D": (re.compile(r"\d+\.\d+(-\d+){1}"), STRONG_MATCH),  # 3.6-1
    "E": (re.compile(r"\d+\.\d+(-\d+){2}"), STRONG_MATCH),  # 3.6-1-1
    "F": (re.compile(r"\d+\.\d+(-\d+){4}"), STRONG_MATCH),  # 3.6-1-1-0-1
}

pattern_quote = {"G": (re.compile(r"\d+\.\d+(-\d+)+"), STRONG_MATCH),}  # номер расценки '3.1-1-5'
pattern_quote.update(pattern_common_bc)
pattern_quote.update(pattern_common_def)

pattern_table = {
    "G": (re.compile(r"^\s*$"), STRONG_MATCH),  # пустая строка
    "H": (re.compile(r"Таблица \d+\.\d+-\d+\."), SOFT_MATCH),
    "L": (re.compile(r"Дополнительные расценки"), STRONG_MATCH),
    "O": (re.compile(r"Атрибуты"), STRONG_MATCH),
}
pattern_table.update(pattern_common_bc)
pattern_table.update(pattern_common_def)

pattern_collection = {}
pattern_collection.update(pattern_common_bc)
pattern_collection.update({
    "D": (re.compile(r"^\s*$"), STRONG_MATCH),  # пустая строка
    "E": (re.compile(r"^\s*$"), STRONG_MATCH),  # пустая строка
    "F": (re.compile(r"^\s*$"), STRONG_MATCH),  # пустая строка
    "H": (re.compile(r"Сборник  \d+\."), SOFT_MATCH),
})


# example_dict = {1:'a', 2:'b', 3:'c', 4:'d'}
#
# for i, k in enumerate(example_dict):
#     print(i, k, example_dict[k])
#
# for i in example_dict:
#     print(i, example_dict[i])


import contextlib, io

s = io.StringIO()
with contextlib.redirect_stdout(s):
    print("jhdjkasdcjascn sdcnasdncsanc")
    print("dkfsfd;k ;lkfa;lkf")


print(s.getvalue())