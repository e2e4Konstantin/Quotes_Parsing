from difflib import SequenceMatcher, get_close_matches


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


bywords = ['Атрибуты', 'Астрибуты', 'Атибуты', 'Атрибуты', 'Атрибуты', 'Атрибуы', 'Aтрибуы', 'Арибуты']



w = 'Атрибуты'   #,'Атрибуы'
print([w==ratio for ratio in bywords])

variants = get_close_matches(w, bywords)
print(variants)

# for x in bywords:
#     print(similar(w, x))

print([SequenceMatcher(None, w, ratio).ratio() for ratio in bywords])
print(min([SequenceMatcher(None, w, ratio).ratio() for ratio in bywords]))
