from typing import Any

from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from utils import delete_file, save_obj_with_image

from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(instance: User, created: bool, **kwargs: Any) -> None:
    """
    Создаём профиль при создании пользователя.

    :param instance: Пользователь.
    :param created: Создан ли пользователь.
    :param kwargs: Any.
    :return: None.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(instance: User, **kwargs: Any) -> None:
    """
    Сохраняем данные профиля при сохранении данных пользователя.

    :param instance: Пользователь.
    :param kwargs: Any.
    :return: None.
    """
    instance.profile.save()


@receiver(pre_delete, sender=User)
def delete_avatar_file_with_user_delete(instance: User, **kwargs: Any) -> None:
    """
    Удаляем файл аватарки, при удалении пользователя.

    :param instance: Пользователь.
    :param kwargs: Any.
    :return: None.
    """
    if instance.profile and instance.profile.avatar:
        delete_file(instance.profile.avatar.path)


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


@receiver(pre_save, sender=Profile)
def get_id_profile_for_image_file(instance: Profile, **kwargs: Any) -> None:
    """
    Если при создании профиля уже содержится изображение,
    то функция предварительно получит id профиля, необходимое для получения директории хранения изображения.

    :param instance: Profile.
    :param kwargs: Any.
    :return: None.
    """
    if not instance.pk and instance.avatar:
        save_obj_with_image(instance, "avatar")
