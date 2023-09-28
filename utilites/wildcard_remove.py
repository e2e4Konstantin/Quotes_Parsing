import re


def wildcard_remove(code: str = None) -> str | None:
    """ Удаляет из строки все символы кроме допустимых """
    return re.sub(r'([.-])\1+', r'\1', re.sub("[^0-9-.]+", r"", code)) if code else None


# "\".*\""  this string starts and end with a double quote

def string_cleaning_capitalize(src_text: str) -> str:
    """ Очищает строку от спецсимволов, двойных пробелов и делает первую букву Прописной. """
    if isinstance(src_text, str):
        return re.sub(r"\s+", ' ', re.sub("^\s+|\n|\r|\t|\v|\f|\s+$", '', src_text)).capitalize()
    return src_text


def drop_quotation(src_text: str) -> str:
    """ Удаляем одинарные и двойные кавычки в начале и в конце"""
    if isinstance(src_text, str):
        return re.sub(r"^[\"']|[\"']$", '', src_text.strip())
    return src_text


if __name__ == "__main__":
    print(string_cleaning_capitalize("   'balabla\n   z  zz' "))
    s = r'"ст  аль -        полиэтилен"'
    print(drop_quotation(s))
    print(string_cleaning_capitalize(drop_quotation(s)))

    sm1=string_cleaning_capitalize(s)
    print(sm1)

    s = '  сталь-полиэтилен'
    print(string_cleaning_capitalize(s))
