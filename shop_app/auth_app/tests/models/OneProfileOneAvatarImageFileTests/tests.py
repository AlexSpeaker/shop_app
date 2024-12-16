import os.path

from django.contrib.auth.models import User
from django.test import TestCase

from shop_app import settings


class OneProfileOneAvatarImageFileTests(TestCase):
    """
    Тест для сигналов модели Profile.
    """

    def test_one_profile_one_avatar_image_file(self) -> None:
        """
        Правило одно.
        Количество пользователей с аватаркой должно быть равно количеству файлов этих аватарок.

        :return: None.
        """
        media_path = settings.MEDIA_ROOT
        profile_media_path = os.path.join(media_path, "profile")
        users_count_with_avatar = (
            User.objects.select_related("profile")
            .filter(profile__avatar__isnull=False)
            .count()
        )
        count_avatar_files = 0
        for _, _, files in os.walk(profile_media_path):
            count_avatar_files += len(files)
        self.assertEqual(count_avatar_files, users_count_with_avatar)
