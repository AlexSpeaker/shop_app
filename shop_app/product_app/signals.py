from typing import Any

from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from product_app.models import Category, ProductImage, SubCategory
from utils import delete_file


@receiver(pre_delete, sender=ProductImage)
def delete_image_file_when_deleting_model_product_image(
    instance: ProductImage, **kwargs: Any
) -> None:
    """
    Удаляем файл изображения, при удалении модели ProductImage.

    :param instance: ProductImage.
    :param kwargs: Any.
    :return: None.
    """
    if instance.image:
        delete_file(instance.image.path)


@receiver(pre_save, sender=ProductImage)
def delete_image_file_when_saving_model_product_image(
    instance: ProductImage, **kwargs: Any
) -> None:
    """
    Удаляем файл изображения, если при сохранении он отличается.

    :param instance: ProductImage.
    :param kwargs: Any.
    :return: None.
    """
    if instance.pk:
        old_instance = ProductImage.objects.get(pk=instance.pk)
        if old_instance.image and old_instance.image != instance.image:
            delete_file(old_instance.image.path)


@receiver(pre_delete, sender=Category)
def delete_image_file_when_deleting_model_category(
    instance: Category, **kwargs: Any
) -> None:
    """
    Удаляем файл изображения, при удалении модели Category.

    :param instance: Category.
    :param kwargs: Any.
    :return: None.
    """
    if instance.image:
        delete_file(instance.image.path)


@receiver(pre_save, sender=Category)
def delete_image_file_when_saving_model_category(
    instance: Category, **kwargs: Any
) -> None:
    """
    Удаляем файл изображения, если при сохранении он отличается.

    :param instance: Category.
    :param kwargs: Any.
    :return: None.
    """
    if instance.pk:
        old_instance = Category.objects.get(pk=instance.pk)
        if old_instance.image and old_instance.image != instance.image:
            delete_file(old_instance.image.path)


@receiver(pre_delete, sender=SubCategory)
def delete_image_file_when_deleting_model_subcategory(
    instance: SubCategory, **kwargs: Any
) -> None:
    """
    Удаляем файл изображения, при удалении модели SubCategory.

    :param instance: SubCategory.
    :param kwargs: Any.
    :return: None.
    """
    if instance.image:
        delete_file(instance.image.path)


@receiver(pre_save, sender=SubCategory)
def delete_image_file_when_saving_model_subcategory(
    instance: SubCategory, **kwargs: Any
) -> None:
    """
    Удаляем файл изображения, если при сохранении он отличается.

    :param instance: SubCategory.
    :param kwargs: Any.
    :return: None.
    """
    if instance.pk:
        old_instance = SubCategory.objects.get(pk=instance.pk)
        if old_instance.image and old_instance.image != instance.image:
            delete_file(old_instance.image.path)
