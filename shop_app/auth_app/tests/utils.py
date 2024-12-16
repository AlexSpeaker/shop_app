import json
from pathlib import Path
from random import choices
from string import ascii_letters
from typing import Dict

from django.contrib.auth.models import User


def get_user_data_from_frontend(new_user_data: Dict[str, str]) -> Dict[str, list[str]]:
    """
    Преобразует данные в тот вид, в котором они приходят от frontend.

    :return: Данные пользователя.
    """
    new_user_key_str: str = json.dumps(new_user_data)
    return {
        new_user_key_str: [""],
    }


def get_user_with_profile() -> User:
    """
    Функция создаёт пользователя вместе с его профилем.

    :return: User.
    """
    user = User.objects.create_user(
        username="".join(choices(ascii_letters, k=6)),
        password="".join(choices(ascii_letters, k=6)),
    )
    user.profile.name = "E".join(choices(ascii_letters, k=6))
    user.profile.surname = "E".join(choices(ascii_letters, k=6))
    user.profile.patronymic = "E".join(choices(ascii_letters, k=6))
    user.profile.email = "E".join(["".join(choices(ascii_letters, k=10)), "@gmail.com"])
    user.profile.phone = "1".join(choices("0123456789", k=9))
    user.save()
    return user


def count_files_in_directory(path: str) -> int:
    """
    Функция возвращает количество файлов в указанной директории.
    :param path: Путь к директории.
    :return: Количество файлов.
    """
    path_obj = Path(path)
    if not path_obj.exists():
        return 0
    return sum(1 for item in path_obj.iterdir() if item.is_file())
