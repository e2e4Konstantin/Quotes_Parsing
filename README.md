# Парсинг (получение данных) из файлов с параметризованными расценками и ресурсами

Места расположения и названия фалов задаются в файле Quotes_Parsing\config\work_place_config.py
Расценки и ресурсы расположены в отдельных файлах для каждой главы и периода.
(Машины_2_68.xlsx, Оборудование_1_13.xlsx, Расценки_3_68.xlsx)

## Обработчики для каждого типа данных
    -  для расценок: quotes_handling(data, sheet_name='name')
    -  для машин: machines_handling(data, 'data')
    -  для материалов: materials_equipment_handling
    -  для оборудования: materials_equipment_handling(data, sheet_name='data', item_name='Equipment')


## потоковая обработка файлов с расценками (по списку)

    stream_quotes_handling(files_path[:4], sheet_name='name')

## Идея

Файл обрабатывается в несколько проходов:
- главы
- сборники
- отделы
- разделы
- таблицы

Для таблиц запоминаются координаты и считывается шапка (названия) атрибутов и параметров.
Проход по всем таблицам и считывание расценок, параметров и атрибутов.

Привязка к названиям столбцов и групп столбцов.
Зашита от сдвигов колонок частичная.

## Валидация данных

проверяются шифры расценок по шаблону, числа там где они должны быть по смыслу

## Результат
создается файл где на отдельных страницах выведены атрибуты, параметры, таблицы.

