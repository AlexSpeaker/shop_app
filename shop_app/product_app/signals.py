from typing import Any

from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from product_app.models import Category, ProductImage, SubCategory
from utils import delete_file, save_obj_with_image


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


@receiver(pre_save, sender=ProductImage)
def get_id_product_image_for_image_file(instance: ProductImage, **kwargs: Any) -> None:
    """
    Если при создании ProductImage уже содержится изображение,
    то функция предварительно получит id ProductImage, необходимое для получения директории хранения изображения.

    :param instance: ProductImage.
    :param kwargs: Any.
    :return: None.
    """
    if not instance.pk and instance.image:
        save_obj_with_image(instance, "image")


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


@receiver(pre_save, sender=Category)
def get_id_category_for_image_file(instance: Category, **kwargs: Any) -> None:
    """
    Если при создании категории уже содержится изображение,
    то функция предварительно получит id категории, необходимое для получения директории хранения изображения.

    :param instance: Category.
    :param kwargs: Any.
    :return: None.
    """
    if not instance.pk and instance.image:
        save_obj_with_image(instance, "image")


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


@receiver(pre_save, sender=SubCategory)
def get_id_subcategory_for_image_file(instance: SubCategory, **kwargs: Any) -> None:
    """
    Если при создании подкатегории уже содержится изображение,
    то функция предварительно получит id подкатегории, необходимое для получения директории хранения изображения.

    :param instance: SubCategory.
    :param kwargs: Any.
    :return: None.
    """
    if not instance.pk and instance.image:
        save_obj_with_image(instance, "image")
