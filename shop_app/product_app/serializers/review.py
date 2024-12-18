from rest_framework import serializers

from product_app.models import Review


class ReviewSerializer(serializers.ModelSerializer[Review]):
    """
    Serializer для модели Review.
    """

    date = serializers.DateTimeField(source='created_at')

    class Meta:
        model = Review
        fields = 'author', 'email', 'text', 'rate', 'date'
