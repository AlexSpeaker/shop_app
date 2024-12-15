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
    **avatar** - Аватарка пользователя.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(
        _("name"), max_length=50, blank=True, null=False, default=""
    )
    surname = models.CharField(
        _("surname"), max_length=50, blank=True, null=False, default=""
    )
    patronymic = models.CharField(
        _("patronymic"), max_length=50, blank=True, default="", null=False
    )
    phone = models.CharField(
        _("phone"), max_length=17, blank=True, default="", null=False
    )
    email = models.EmailField(
        _("email"), max_length=254, blank=True, default="", null=False
    )
    avatar = models.ImageField(
        _("avatar"),
        null=True,
        blank=True,
        upload_to=avatar_directory_path,
        default=None,
    )

    @property
    def full_name(self) -> str:
        """
        Функция вернёт полное ФИО пользователя.

        :return: ФИО пользователя.
        """
        return " ".join([self.surname, self.name, self.patronymic]).strip()

    @full_name.setter
    def full_name(self, value: str) -> None:
        """
        Функция принимает строку и распределяет данные между surname, name, patronymic.
        Распределение такое:
        - Если передано 1 слово - это будет name.
        - Если передано 2 слова - это будет surname, name соответственно.
        - Если передано 3 слова - это будет surname, name, patronymic соответственно.
        - Учитываются только первые 3 слова, остальные игнорируются.

        :param value: Строка с данными.
        :return: None.
        """

        full_name_list = value.strip().split()
        if len(full_name_list) >= 3:
            self.surname, self.name, self.patronymic = full_name_list[:3]
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

    def __str__(self) -> str:
        """
        Строковое представление.
        :return: ФИО.
        """
        return self.full_name

    def __repr__(self) -> str:
        """
        Строковое представление для отладки.
        :return: Profile(ФИО).
        """
        return f"Profile({self.full_name})"
