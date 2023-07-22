from dataclasses import dataclass, field, fields
import re


@dataclass
class Header:
    """Заголовок"""
    name_header: str = ""  # название
    column_header: int = 0  # номер колонки


@dataclass
class HeaderOption:
    """ Заголовок таблицы параметров """
    column_header_option: int = 0  # первая колонка заголовка параметров
    name_header_option: str = ""  # название таблицы параметров
    option_headers: list[Header] = field(default_factory=list)  # список заголовков параметров


@dataclass
class TableItem:
    """ Таблица """
    cod_table: str = ""  # код таблицы
    number_table: str = ""  # номер таблицы из колонки с названием
    name_table: str = ""  # название
    row_table: int = 0  # номер строки
    catalog_table: list[str] = field(default_factory=list)  # ссылки на каталог
    attribute_table: list[Header] = field(default_factory=list)  # список заголовков атрибутов
    options_table: list[HeaderOption] = field(default_factory=list)  # список заголовков параметров

    def __str__(self):
        return f"row:{self.row_table:4}, {self.number_table:8}, атрибутов: {len(self.attribute_table)}, " \
               f"параметров: {len(self.options_table)}, {self.name_table}, {self.cod_table}, " \
               f"{self.attribute_table}, {self.options_table}"

    def to_list(self) -> list:
        catalog = ', '.join(x for x in self.catalog_table)
        attributes = ', '.join(x.name_header for x in self.attribute_table)
        option = ', '.join(x.name_header_option for x in self.options_table)
        return [self.row_table, self.number_table, self.cod_table, len(self.attribute_table), len(self.options_table),
                self.name_table, attributes, option]


@dataclass
class Attribute:
    """ Атрибут """
    name_attribute: str = ""
    value_attribute: str = ""


@dataclass
class Option:
    """ Параметр """
    name_option: str = ""
    value_option: list[tuple[str, str]] = field(default_factory=list)  # (название, значение)


@dataclass
class Quote:
    """ Расценка """
    row_quote: int = -1
    table_quote: str = ""
    cod_quote: str = ""
    name_quote: str = ""
    sizer_quote: str = ""
    statistics_quote: int = 0
    parameterized_quote: bool = False
    type_quote: str = ""
    parent_quote: str = ""

    attributes_quote: list[Attribute] = field(default_factory=list)
    options_quote: list[Option] = field(default_factory=list)

    def __str__(self):
        s = '; '.join(f'{x.name}={getattr(self, x.name)!r}' for x in fields(self))
        return f'{type(self).__name__}({s})'

    def short_str(self):
        s = f"{self.cod_quote}; {self.name_quote}; {self.table_quote}; {self.parameterized_quote}; " \
            f"{self.attributes_quote}; {self.options_quote};"
        return s

    def debug_str(self):
        return f"Расценка: {self.cod_quote}. Таблица: {self.table_quote}. " \
               f"Атрибутов: {len(self.attributes_quote)}. Параметров: {len(self.options_quote)}. " \
               f"Параметризация: {'++' if self.parameterized_quote else '--'}"

    def csv_list(self):
        return [getattr(self, x.name) for x in fields(self)]

    def options_control(self, limit_quantity: int = 5) -> None:
        # variants = ["до", "тип значения", "тип"]

        pattern = [
            re.compile(r"^от"),
            re.compile(r"^до"),
            re.compile(r"^ед[\.\s]\s?изм"),
            re.compile(r"^шаг"),
            re.compile(r"^тип"),
        ]

        main_header_option = ["от", "до (включительно)", "Ед. изм.", "Шаг", "Тип диапазона значений"]
        main_header_option = [x.strip().lower() for x in main_header_option]
        line_main_header = " ".join(main_header_option)

        error_set = []
        red = "\u001b[31m"
        reset = "\u001b[0m"
        yellow = "\u001b[38;5;11m"
        for option in self.options_quote:
            error_quantity = ""
            error_header = ""
            error_place = ""
            header = [x[0].strip().lower() for x in option.value_option]
            line_header = " ".join(header)

            if len(option.value_option) > limit_quantity:
                # error_quantity = f"У параметра: '{red}{option.name_option}{reset}' расценки: {self.cod_quote} больше {red}{limit_quantity}{reset} значений. Всего: {red}{len(option.value_option)}{reset}"
                error_quantity = f"У параметра: '{option.name_option}' расценки: {self.cod_quote} больше {limit_quantity} значений. Всего: {len(option.value_option)}"

            result_match = set()
            for i in range(len(pattern)):
                result = pattern[i].match(header[i])
                result_match.add(True) if result else result_match.add(False)
            if not all(result_match):
                # error_header = f"У параметра: '{yellow}{option.name_option}{reset}' для расценки: {self.cod_quote} " \
                #                f"нетиповой заголовок: '{yellow}{line_header}{reset}' / '{line_main_header}'"
                error_header = f"У параметра: '{option.name_option}' для расценки: {self.cod_quote} " \
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

            tmp = [x for x in [error_quantity, error_header] if x]
            if len(tmp) > 0:
                error_set.append("\n".join(tmp))

        if len(error_set) > 0:
            print("\n".join(error_set))








@dataclass
class Collection:
    """ Сборник """
    row_start: int
    cod: str
    name: str
    quantity_parameterized_quotes: int = 0
    quantity_not_parameterized_quotes: int = 0
    not_parameterized_list: list[str] = field(default_factory=list)


    def __str__(self):
        s = '; '.join(f'{x.name}={getattr(self, x.name)!r}' for x in fields(self))
        return f'{type(self).__name__}({s})'


@dataclass
class Resource:
    row: int
    a_column: int
    origin: str
    press_mark: str
    title: str
    measuring_unit: str
    use_count: int
    parameterization: bool
    attributes_resource: list[Attribute] = field(default_factory=list)
    options_resource: list[Option] = field(default_factory=list)

    def __str__(self):
        s = '; '.join(f'{x.name}={getattr(self, x.name)!r}' for x in fields(self))
        return f'{type(self).__name__}({s})'




QUOTE_TYPE: list[str] = ["основная", "дополнительная"]

tables: dict[str, TableItem] = dict()
failed_tables: list[tuple[int, str]] = list()
quotes: list[Quote] = list()
heap: list[Quote] = list()
collections: dict[str, Collection] = dict()
resource_data: list[Resource] = list()
resource_tables: list[TableItem] = list()
