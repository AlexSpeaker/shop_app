from django.contrib.auth.models import User
from django.db import models


def avatar_directory_path(instance: "Profile", filename: str) -> str:
    """
    Генератор относительного пути для сохранения файла изображения для модели Profile.
    :param instance: Экземпляр Profile.
    :param filename: Название файла.
    :return: Относительный путь к файлу.
    """
    return "profile/{user_id}/avatar/{filename}".format(
        user_id=instance.user.pk, filename=filename
    )


class Profile(models.Model):
    """
    Продолжение профиля пользователя.

    **user** - Сам пользователь. \n
    **phone** - Телефон пользователя. \n
    **avatar** - Относительный путь к аватарке пользователя.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=17, default=None, null=True)
    avatar = models.ImageField(
        null=True, blank=True, upload_to=avatar_directory_path, default=None
    )
