import re
pattern = [
    re.compile(r"^от"),
    re.compile(r"^до"),
    re.compile(r"^ед[\.\s]\s?изм"),
    re.compile(r"^шаг"),
    re.compile(r"^тип"),
]



main_header_option = ["от", "до (включительно)", "Ед. изм.", "Шаг", "Тип диапазона значений"]
main_header_option = [x.strip().lower() for x in main_header_option]

test = [" от x", " до ", " Ед.изм", "Шаг ", " Тип *"]
test = [x.strip().lower() for x in test]


print(test)
result_match = set()

for i in range(len(pattern)):
    result = pattern[i].match(test[i])
    result_match.add(True) if result else result_match.add(False)

print(result_match)
print(all(result_match))

#
# print(main_header_option)
# for i in range(len(pattern)):
#     result = pattern[i].match(main_header_option[i])
#     print(result)
