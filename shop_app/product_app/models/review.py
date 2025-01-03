from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from product_app.models import Product


class Review(models.Model):
    """
    Модель отзыва.

    **author** - Имя пользователя (вводит сам). \n
    **email** - Email пользователя (вводит сам). \n
    **product** - Продукт. \n
    **text** - Текст отзыва. \n
    **created_at** - Дата написания отзыва. \n
    **rate** - Оценка.
    """

    author = models.CharField(max_length=100, blank=True, null=False)
    email = models.EmailField(max_length=100, blank=True, null=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    text = models.TextField(_("text"), null=False, blank=False, max_length=5000)
    date = models.DateTimeField(
        _("created at"), null=False, blank=False, auto_now_add=True
    )
    rate = models.IntegerField(
        _("rate"),
        null=False,
        blank=False,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )

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
