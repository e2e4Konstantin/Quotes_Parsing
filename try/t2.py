tab_color = ["0099CC00", "00FFCC00", "00FF9900", "00FF6600", "00666699",
             "00C0C0C0", ]
items = ["Tables", "Quote", "Attributes", "Options", "Collections", "Header"]

d = dict(zip(items, tab_color))
f = {k: v for k, v in zip(items, tab_color)}
print(d)
print(f)
items.sort()
print(items)