from typing import Any, Dict

from order_app.serializers.utils import (
    CardNumberValidator,
    CodeValidator,
    ExpiryDateValidator,
    MonthValidator,
    NameValidator,
    YearValidator,
)
from rest_framework import serializers


class InPaymentSerializer(serializers.Serializer[Dict[str, Any]]):
    """
    Serializer Payment входящих данных.
    """
    number = serializers.CharField(
        max_length=16, required=True, validators=[CardNumberValidator()]
    )
    name = serializers.CharField(
        max_length=100, required=True, validators=[NameValidator()]
    )
    month = serializers.ChoiceField(
        choices=[str(i).zfill(2) for i in range(1, 13)],
        required=True,
        validators=[MonthValidator()],
    )
    year = serializers.IntegerField(required=True, validators=[YearValidator()])
    code = serializers.CharField(
        max_length=3, required=True, validators=[CodeValidator()]
    )

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Дополнительная валидация для проверки срока действия карты.

        :param data: Dict[str, Any].
        :return: Dict[str, Any].
        """
        ExpiryDateValidator()(data)
        return data
