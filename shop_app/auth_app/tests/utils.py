import json
from typing import Dict


def get_user_data_from_frontend(new_user_data: Dict[str, str]) -> Dict[str, list[str]]:
    """
    Преобразует данные в тот вид, в котором они приходят от frontend.

    :return: Данные пользователя.
    """
    new_user_key_str: str = json.dumps(new_user_data)
    return {
        new_user_key_str: [""],
    }
