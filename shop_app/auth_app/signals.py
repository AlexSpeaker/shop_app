from typing import Any

from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from utils import delete_file

from .models import Profile


@receiver(pre_delete, sender=Profile)
def delete_avatar_file_with_profile_delete(instance: Profile, **kwargs: Any) -> None:
    """
    Удаляем файл аватарки, при удалении профиля.

    :param instance: Профиль пользователя.
    :param kwargs: Any.
    :return: None.
    """
    if instance.avatar:
        delete_file(instance.avatar.path)


@receiver(pre_save, sender=Profile)
def delete_avatar_file_with_save_profile(instance: Profile, **kwargs: Any) -> None:
    """
    Удаляем файл аватарки, при сохранении профиля, если аватарка была изменена.

    :param instance: Профиль пользователя.
    :param kwargs: Any.
    :return: None.
    """
    if instance.pk:
        old_instance = Profile.objects.get(pk=instance.pk)
        if old_instance.avatar and old_instance.avatar != instance.avatar:
            delete_file(old_instance.avatar.path)
