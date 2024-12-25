import json
import os
import re
import uuid
from json import JSONDecodeError
from typing import Any, Dict, TypeVar, Optional

from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import QuerySet
from django.http import QueryDict
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request


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


def parser_query_params(query_params: QueryDict) -> Dict[str, Any]:
    """
    Функция преобразует параметры типа: param_name[param_sub_name] = value,
    в параметр param_name со своим словарём {param_sub_name: value},
    а также param_name[] = value в список param_name = [value1, value2, ...].

    :param query_params: Query параметры в виде словаря.
    :return: Dict[str, Any]
    """
    response_dict: Dict[str, Any] = {}
    for key, value in query_params.items():
        pattern_dict = r"^([^\[]+)\[([^\]]+)\]$"
        pattern_list = r"^([^\[]+)\[\]$"
        match_dict = re.match(pattern_dict, key)
        match_list = re.match(pattern_list, key)
        if match_dict:
            response_dict.setdefault(match_dict.group(1), {})[
                match_dict.group(2)
            ] = value
        elif match_list:
            response_dict.setdefault(match_list.group(1), []).extend(
                query_params.getlist(f"{match_list.group(1)}[]")
            )
        else:
            response_dict[key] = value

    return response_dict


T = TypeVar("T", bound=models.Model)


def get_or_none(queryset: QuerySet[T], **kwargs: Any) -> T | None:
    """
    Функция вернёт объект модели, если такой будет найден, иначе None.

    :param queryset: Queryset модели.
    :param kwargs: Параметры объекта.
    :return: Объект модели, если такой будет найден, иначе None.
    """
    try:
        obj: T = queryset.get(**kwargs)
    except ObjectDoesNotExist:
        return None
    return obj

def get_or_create_anonymous_session_id(request: Request) -> Optional[str]:
    """
    Вернёт уникальный anonymous_session_id для анонимного пользователя.
    Если его не существует, то создаст его.
    В случае, если пользователь прошёл аутентификацию, то вернёт None.

    :param request: Request.
    :return: Уникальный anonymous_session_id,
        если пользователь не прошёл аутентификацию, иначе None.
    """
    if request.user.is_authenticated:
        return None
    anonymous_session_id = request.session.get("anonymous_session_id")
    if anonymous_session_id:
        return anonymous_session_id
    anonymous_session_id = uuid.uuid4().hex
    request.session["anonymous_session_id"] = anonymous_session_id
    return anonymous_session_id
