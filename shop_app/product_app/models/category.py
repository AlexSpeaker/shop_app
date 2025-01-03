import os
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


def category_image_directory_path(instance: "Category", filename: str) -> str:
    """
    Генератор относительного пути для сохранения файла изображения для модели Category.
    :param instance: Экземпляр Category.
    :param filename: Название файла.
    :return: Относительный путь к файлу.
    """

    return os.path.join("categories", str(instance.unique_id), "images", filename)


class Category(models.Model):
    """
    Модель категории.

    **name** - Имя категории.
    """

    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(
        _("name"), max_length=100, unique=True, null=False, blank=False
    )
    image = models.ImageField(
        _("image"), null=True, blank=False, upload_to=category_image_directory_path
    )

    def __str__(self) -> str:
        """
        Строковое представление.

        :return: Имя.
        """
        return self.name

    def __repr__(self) -> str:
        """
        Строковое представление для отладки.

        :return: Category(Имя).
        """
        return f"Category({self.name})"

    class Meta:
        """
        Метаданные.
        """

        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ("name",)
