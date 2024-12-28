from datetime import datetime
from typing import Any, Dict

from django.utils import timezone
from rest_framework.exceptions import ValidationError


class CardNumberValidator:
    def __call__(self, value: Any) -> None:
        """
        Валидатор для номера карты.

        :param value: Предполагаемый номер карты.
        :return: None.
        """
        if len(value) != 16 or not value.isdigit():
            raise ValidationError("Номер карты должен содержать 16 цифр.")


class NameValidator:
    def __call__(self, value: Any) -> None:
        """
        Валидатор для имени владельца карты.

        :param value: Предполагаемое имя владельца карты.
        :return: None.
        """
        if not value.strip():
            raise ValidationError("Имя владельца карты не может быть пустым.")


class MonthValidator:
    def __call__(self, value: Any) -> None:
        """
        Валидатор для месяца.

        :param value: Предполагаемый месяц.
        :return: None.
        """
        if int(value) < 1 or int(value) > 12:
            raise ValidationError("Месяц должен быть от 01 до 12.")


class YearValidator:
    def __call__(self, value: Any) -> None:
        """
        Валидатор для года.

        :param value: Предполагаемый год.
        :return: None.
        """
        current_year = timezone.now().year
        if value < current_year:
            raise ValidationError("Год должен быть не меньше текущего года.")


class CodeValidator:
    def __call__(self, value: Any) -> None:
        """
        Валидатор для CVV-кода.

        :param value: Предполагаемый CVV-код.
        :return: None.
        """
        if len(value) != 3 or not value.isdigit():
            raise ValidationError("CVV-код должен содержать 3 цифры.")


class ExpiryDateValidator:
    def __call__(self, data: Dict[str, Any]) -> None:
        """
        Валидатор для проверки даты действия карты.

        :param data: Данные присланные пользователем.
        :return: None.
        """
        month = int(data["month"])
        year = int(data["year"])
        current_date = timezone.now()
        expiry_date = datetime(year, month, 1, tzinfo=current_date.tzinfo)

        if expiry_date < current_date:
            raise ValidationError("Срок действия карты истек.")
