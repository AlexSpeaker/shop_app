import json
from typing import Any, Dict


def get_user_data(data: Dict[str, str]) -> Dict[str, Any]:
    """
    Функция из ключа словаря извлекает словарь (да, данные почему-то приходят именно так),
    нормализует его под данные пользователя и возвращает их.

    :param data: Пришедшие данные из request.
    :return: Словарь с данными пользователя.
    """
    return json.loads(list(data.keys())[0]) if len(data.keys()) == 1 else data
