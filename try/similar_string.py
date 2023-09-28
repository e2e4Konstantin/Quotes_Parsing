from difflib import SequenceMatcher, get_close_matches


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


t = ['кВ', 'кВ·А', 'кВ•А', 'кВА', 'кВт']
# for i in range(len(t)):
#     print(similar(t[0], t[i]))
# print()
# for i in range(len(t)):
#     print(similar(t[1], t[i]))


d = ['м.', 'м', 'мм', 'мм.', 'м/мин', 'м/с', 'м2', 'м3', 'м3/мин', 'м3/сут', 'м3/ч']
for i in range(len(d)):
    print(f"{d[0]} {d[i]} = {similar(d[0], d[i])}")


print(get_close_matches('appel', ['ape', 'apple', 'peach', 'puppy']))
print(get_close_matches('мм', d))










#
#
# import jellyfish
# >>> jellyfish.levenshtein_distance(u'jellyfish', u'smellyfish')
# 2
# >>> jellyfish.jaro_distance(u'jellyfish', u'smellyfish')
# 0.89629629629629637




