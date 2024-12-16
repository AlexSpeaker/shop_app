import os

from django.db import models
from django.utils.translation import gettext_lazy as _
from product_app.models.product import Product


def product_image_directory_path(instance: "ProductImage", filename: str) -> str:
    """
    Генератор относительного пути для сохранения файла изображения для модели ProductImage.
    :param instance: Экземпляр ProductImage.
    :param filename: Название файла.
    :return: Относительный путь к файлу.
    """
    return os.path.join(
        "product_image", str(instance.product.pk), str(instance.pk), filename
    )


class ProductImage(models.Model):
    """
    Модель изображения продукта.

    **title** - Краткое описание (будет показано, если вдруг изображение будет не доступно). \n
    **image** - Изображение продукта. \n
    **product** - Продукт. \n
    """

    title = models.CharField(_("title"), max_length=500, null=False, blank=False)
    image = models.ImageField(
        _("image"), null=True, blank=False, upload_to=product_image_directory_path
    )
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
