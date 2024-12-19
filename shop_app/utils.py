import json
import os
import re
from json import JSONDecodeError
from typing import Any, Dict

from django.core.validators import RegexValidator
from rest_framework.exceptions import ValidationError


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


class PhoneValidator(RegexValidator):
    """
    Класс-валидатор номера телефона.
    """

    def __init__(self) -> None:
        regex = r"^\+?1?\d{9,15}$"
        message = "Номер телефона должен быть введен в формате: '+9999999999'. Допускается количество цифр не более 15."
        super().__init__(regex=regex, message=message)


def delete_file(path: str) -> None:
    """
    Функция удаляет файл.

    :param path: Путь к файлу.
    :return: None.
    """
    if os.path.isfile(path):
        os.remove(path)


class PasswordValidator:
    """
    Класс-валидатор для пароля.
    """

    def __init__(self) -> None:
        self.min_length = 8
        self.max_length = 50
        self.message = (
            f"Пароль должен содержать не менее {self.min_length} символов, "
            f"пароль должен содержать не более {self.max_length} символов."
        )

    def __call__(self, value: str) -> None:
        """
        Список проверок.

        :param value: Пароль.
        :return: None.
        """

        # Проверка длины пароля
        if len(value) < self.min_length or len(value) > self.max_length:
            raise ValidationError(self.message)


def parser_query_params(query_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Функция преобразует параметры типа: param_name[param_sub_name],
    в параметр param_name со своим словарём {sub_name: value}.

    :param query_params: Query параметры в виде словаря.
    :return: Dict[str, Any]
    """
    response_dict: Dict[str, Any] = {}
    for key, value in query_params.items():
        pattern = r"^([^\[]+)\[([^\]]+)\]$"
        match = re.match(pattern, key)
        if match:
            response_dict.setdefault(match.group(1), {})[match.group(2)] = value
        else:
            response_dict[key] = value
    return response_dict
