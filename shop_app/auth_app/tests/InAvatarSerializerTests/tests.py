from pathlib import Path

from auth_app.serializers import InAvatarSerializer
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase


class InAvatarSerializerTests(APITestCase):
    """
    Класс Тест для сериализатора InAvatarSerializer.
    """

    files_for_test_dir = Path(__file__).parent.parent / "files_for_test"
    valid_file_path = files_for_test_dir / "valid_file.png"
    invalid_file_path = files_for_test_dir / "no_valid_file.txt"
    serializer_class = InAvatarSerializer

    def test_valid_file(self) -> None:
        """
        Тестируем с валидными данными. Файл является картинкой.

        :return: None.
        """
        with open(self.valid_file_path, "rb") as file:
            data = file.read()
        image_file = SimpleUploadedFile(
            name="test_image.png", content=data, content_type="image/png"
        )
        serializer = self.serializer_class(data={"avatar": image_file})
        self.assertTrue(serializer.is_valid())

    def test_invalid_file(self) -> None:
        """
        Тестируем с невалидными данными. Файл не является картинкой.

        :return: None.
        """
        with open(self.invalid_file_path, "rb") as file:
            data = file.read()
        image_file = SimpleUploadedFile(
            name="test_image.png", content=data, content_type="image/png"
        )
        serializer = self.serializer_class(data={"avatar": image_file})
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
