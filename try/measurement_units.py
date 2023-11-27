# https://habr.com/ru/articles/682306/


# from quantities import units
#
# unit_symbols = [u.symbol for _, u in units.__dict__.items() if isinstance(u, type(units.deg))]
# print(unit_symbols)


# from quantities import units as u
#
# myList = [unit for unit in dir(u.length)
#           if type(getattr(u.length, unit)) is u.UnitLength]
#
# print(myList)

#
# import pint
# ureg = pint.UnitRegistry()
#
# print(ureg, pint.__version__, ureg.Quantity)
# print('MHz' in ureg)
# print('gigatrees' in ureg)
#
# distance = 24.0 * ureg.meter
# print(distance)
# print(distance.units)
# print(distance.dimensionality)
#
# height = 5.0 * ureg.foot + 9.0 * ureg.inch
# print(height)
# print(height.to_base_units())
#
# m = ureg.meter
# v = 1*(m*3)/(m*3)
# print(v)

#
#
# from quantiphy import Quantity
#
# rawdata = '0 450, 10 400, 20 360'
# data = []
# for pair in rawdata.split(','):
#     time, temp = pair.split()
#     time = Quantity(time, 'min', scale='s')
#     temp = Quantity(temp, '°F', scale='K')
#     data += [(time, temp)]
#
# for time, temp in data:
#     print(f'{time:9q} {temp:9q}')
#
# for time, temp in data:
#     print(f"{time:<7smin} {temp:s°F}")
