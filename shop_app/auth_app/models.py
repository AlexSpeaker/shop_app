from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


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
    **name** - Имя. \n
    **surname** - Фамилия. \n
    **patronymic** - Отчество. \n
    **phone** - Телефон пользователя. \n
    **avatar** - Относительный путь к аватарке пользователя.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(_("name"), max_length=50, blank=False, null=False)
    surname = models.CharField(_("surname"), max_length=50, blank=True, default="")
    patronymic = models.CharField(
        _("patronymic"), max_length=50, blank=True, default=""
    )
    phone = models.CharField(_("phone"), max_length=17, default=None, null=True)
    avatar = models.ImageField(
        _("avatar"),
        null=True,
        blank=True,
        upload_to=avatar_directory_path,
        default=None,
    )
