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

red = "\u001b[31m"
reset = "\u001b[0m"
yellow = "\u001b[38;5;11m"
error_quantity = f"У параметра: '{red}{option.name_option}{reset}' расценки: {self.cod_quote} больше {red}{limit_quantity}{reset} значений. Всего: {red}{len(option.value_option)}{reset}"
# error_header = f"У параметра: '{yellow}{option.name_option}{reset}' для расценки: {self.cod_quote} " \
                #                f"нетиповой заголовок: '{yellow}{line_header}{reset}' / '{line_main_header}'"

f"нетиповой заголовок: '{line_header}' / '{line_main_header}'"
# test_header = set(header)
# master_header = set(main_header_option)
# if test_header != master_header:
#     error_header = f"У параметра: '{yellow}{option.name_option}{reset}' для расценки: {self.cod_quote} нетипичный заголовок: '{yellow}{line_header}{reset}' / '{line_main_header}'"
# else:
#     in_place = all([header[x] == main_header_option[x] for x in range(len(main_header_option))])
#     if not in_place:
#         error_place = f"У параметра: '{yellow}{option.name_option}{reset}' для расценки: {self.cod_quote} заголовки переставлены: '{yellow}{line_header}{reset}'"
# error_set.append("\n".join([x for x in [error_quantity, error_header, error_place] if x]))
