from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Review(models.Model):
    """
    Модель отзыва.

    **user** - Пользователь. \n
    **text** - Текст отзыва. \n
    **created_at** - Дата написания отзыва. \n
    **rate** - Оценка.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField(_("text"), null=False, blank=False, max_length=5000)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    rate = models.IntegerField(_("rate"), null=False, blank=False)

    def __str__(self) -> str:
        """
        Строковое представление.

        :return: Первые слова отзыва.
        """
        return f"{self.text[:30]}..."

    def __repr__(self) -> str:
        """
        Строковое представление для отладки.

        :return: Review(Первые слова отзыва).
        """
        return f"Review({self.text[:30]}...)"
