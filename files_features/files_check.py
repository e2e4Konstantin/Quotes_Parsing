import os
from pathlib import Path


def file_unused(abs_file_name: str) -> bool:
    """ Проверяет, занят или нет указанный по абсолютному маршруту файл
        другим приложением. """
    if abs_file_name:
        if os.path.exists(abs_file_name):
            try:
                os.rename(abs_file_name, abs_file_name)
                return True
            except IOError:
                return False
        else:
            return True
    return False


def file_exists(abs_file_name: str) -> bool:
    """ Существует файл или нет. """
    try:
        my_abs_path = Path(abs_file_name).resolve(strict=True)
    except FileNotFoundError:
        return False
    else:
        return True
