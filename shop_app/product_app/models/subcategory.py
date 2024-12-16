from django.db import models
from django.utils.translation import gettext_lazy as _
from product_app.models.category import Category

def subcategory_image_directory_path(instance: "SubCategory", filename: str) -> str:
    """
    Генератор относительного пути для сохранения файла изображения для модели SubCategory.
    :param instance: Экземпляр SubCategory.
    :param filename: Название файла.
    :return: Относительный путь к файлу.
    """
    return "subcategories/{subcategory_id}/images/{filename}".format(
        subcategory_id=instance.pk, filename=filename
    )
class SubCategory(models.Model):
    """
    Модель подкатегории.

    **name** - Имя подкатегории. \n
    **category** - Категория.
    """

    name = models.CharField(
        _("name"), max_length=100, unique=True, null=False, blank=False
    )
    image = models.ImageField(_("image"), upload_to=subcategory_image_directory_path, null=False, blank=False)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="subcategories"
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

        :return: SubCategory(Имя).
        """
        return f"SubCategory({self.name})"

    class Meta:
        """
        Метаданные.
        """

        verbose_name = _("subcategory")
        verbose_name_plural = _("subcategories")
        ordering = ("name",)
