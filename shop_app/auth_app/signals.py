from typing import Any

from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import Profile
from .utils import delete_file


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
def delete_avatar(instance: User, **kwargs: Any) -> None:
    """
    Удаляем файл аватарки, при удалении пользователя.
    :param instance: Пользователь.
    :param kwargs: Any.
    :return: None.
    """
    if instance.profile and instance.profile.avatar:
        delete_file(instance.profile.avatar.path)
