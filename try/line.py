import pprint
import pickle

s = r"""
Диск\1_KK\Job_CNAC\office_targets\tasck_2\sources
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 18245 entries, 0 to 18244
Columns: 57 entries, 0 to 56
dtypes: object(57)
memory usage: 7.9+ MB
None
непустых значений в столбце 'G': 12316 

Прочитано сборников: 41
Прочитано таблиц: 2667
	правильных: 2634
	кривых: 33
Прочитано расценок: 12315
	записано: 6362
	пустые атрибуты и параметры: 5862
	всего расценок в таблицах: 12224
	расценок без таблиц: 91

файл: template_4_68.xlsx, лист: name, папка: F:\Kazak\Google Диск\1_KK\Job_CNAC\office_targets\tasck_2\sources
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 8666 entries, 0 to 8665
Columns: 40 entries, 0 to 39
dtypes: object(40)
memory usage: 2.6+ MB
None
непустых значений в столбце 'G': 6614 

Прочитано сборников: 19
Прочитано таблиц: 930
	правильных: 857
	кривых: 40
Прочитано расценок: 6611
	записано: 3667
	пустые атрибуты и параметры: 2409
	всего расценок в таблицах: 6076
	расценок без таблиц: 535
"""

# pprint.pprint(s.splitlines())
s = ""
with open(r'..\output\out_string.pickle', 'rb') as handle:
    s = pickle.load(handle)

print(len(s))

sl = s.splitlines()

for x in sl:
    print((x, ))