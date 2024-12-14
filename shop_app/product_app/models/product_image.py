from django.db import models
from django.utils.translation import gettext_lazy as _
from product_app.models.product import Product


class ProductImage(models.Model):
    """
    Модель изображения продукта.

    **title** - Краткое описание (будет показано, если вдруг изображение будет не доступно). \n
    **image** - Изображение продукта. \n
    **product** - Продукт. \n
    """

    title = models.CharField(_("title"), max_length=500, null=False, blank=False)
    image = models.ImageField(_("image"), null=False, blank=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )

    def __str__(self) -> str:
        """
        Строковое представление.

        :return: Краткое описание.
        """
        return f"{self.title[:30]}..."

    def __repr__(self) -> str:
        """
        Строковое представление для отладки.

        :return: ProductImage(Краткое описание).
        """
        return f"ProductImage({self.title[:30]}...)"
