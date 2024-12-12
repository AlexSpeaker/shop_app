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
    **email** - Почта пользователя. \n
    **avatar** - Относительный путь к аватарке пользователя.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(_("name"), max_length=50, blank=False, null=False)
    surname = models.CharField(_("surname"), max_length=50, blank=True, default="")
    patronymic = models.CharField(
        _("patronymic"), max_length=50, blank=True, default=""
    )
    phone = models.CharField(_("phone"), max_length=17, blank=True, default="")
    email = models.EmailField(_("email"), max_length=254, blank=True, default="")
    avatar = models.ImageField(
        _("avatar"),
        null=True,
        blank=True,
        upload_to=avatar_directory_path,
        default=None,
    )

    @property
    def fullName(self) -> str:
        return " ".join([self.surname, self.name, self.patronymic]).strip()

    @fullName.setter
    def fullName(self, value: str) -> None:
        full_name_list = value.strip().split()
        if len(full_name_list) == 3:
            self.surname, self.name, self.patronymic = full_name_list
        elif len(full_name_list) == 2:
            self.surname, self.name, self.patronymic = (
                full_name_list[0],
                full_name_list[1],
                "",
            )
        elif len(full_name_list) == 1:
            self.surname, self.name, self.patronymic = (
                "",
                full_name_list[0],
                "",
            )
        else:
            self.surname, self.name, self.patronymic = full_name_list[:3]
