import json
from json import JSONDecodeError
from typing import Any, Dict


def get_user_data(data: Dict[str, str]) -> Dict[str, Any]:
    """
    Функция из ключа словаря извлекает словарь (да, да, данные почему-то от фронта приходят именно так),
    нормализует его под данные пользователя и возвращает их.

    :param data: Пришедшие данные из request.
    :return: Словарь с данными пользователя.
    """
    normalize_data = None
    if len(data.keys()) == 1:
        try:
            normalize_data = json.loads(list(data.keys())[0])
        except (JSONDecodeError, TypeError, ValueError):
            pass

    return normalize_data if normalize_data else data
