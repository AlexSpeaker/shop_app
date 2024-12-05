import json
from typing import Dict


def get_user_data(data: Dict[str, str]) -> Dict[str, str]:
    """
    Функция из ключа словаря извлекает словарь (да, данные почему-то приходят именно так),
    нормализует его под данные пользователя и возвращает их.

    :param data: Пришедшие данные из request.
    :return: Словарь с данными пользователя.
    """
    if not data:
        return {}
    user_data: Dict[str, str] = json.loads(list(data.keys())[0])
    name = user_data.get("name")
    if not name:
        first_name, last_name = "", ""
    else:
        name_split = name.split(" ")
        first_name, last_name = (
            name_split if len(name_split) == 2 else (name_split[0], "")
        )

    normalized_user_data = dict(
        username=user_data.get("username", ""),
        first_name=first_name,
        last_name=last_name,
        password=user_data.get("password", ""),
    )
    return normalized_user_data
