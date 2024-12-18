from rest_framework import serializers

from product_app.models import Review


class ReviewSerializer(serializers.ModelSerializer[Review]):
    """
    Serializer для модели Review.
    """

    date = serializers.DateTimeField(source='created_at', format='%Y-%m-%d %H:%M')

    class Meta:
        model = Review
        fields = 'author', 'email', 'text', 'rate', 'date'

    @staticmethod
    def validate_author(value: str) -> str:
        """
        Проверка имени автора, если имя отсутствует, заменяем его на Anonymous.

        :param value: Введённое имя автора.
        :return: Имя автора, если имя есть, иначе Anonymous.
        """
        return value if value else "Anonymous"
