from typing import Any

from auth_app.utils import delete_file
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from product_app.models import ProductImage


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
        if old_instance.image != instance.image:
            delete_file(old_instance.image.path)

