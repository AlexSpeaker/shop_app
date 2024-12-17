import json
import os
from json import JSONDecodeError
from typing import Any, Dict, TypeVar

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


T = TypeVar("T")


def save_obj_with_image(instance: T, attr: str) -> T:
    """
    Функция предварительно сохранит объект, а потом добавит в него изображение,
    так как для создания директории нужен id объекта.

    :param instance: Объект перед созданием.
    :param attr: Атрибут с изображением.
    :return: Созданный объект.
    """
    image = getattr(instance, attr)
    setattr(instance, attr, None)
    instance.save()
    setattr(instance, attr, image)
    instance.save()
    return instance
