import os.path

from django.contrib.auth.models import User
from django.test import TestCase
from product_app.models import ProductImage

from shop_app import settings


class OneProductImageOneProductImageFileTests(TestCase):
    """
    Тест для сигналов модели ProductImage.
    """

    def test_one_product_image_one_product_image_file(self) -> None:
        """
        Правило одно.
        Количество сущностей ProductImage должно быть равно количеству файлов.

        :return: None.
        """
        media_path = settings.MEDIA_ROOT
        product_image_media_path = os.path.join(media_path, "products")
        product_image_objects_count = ProductImage.objects.all().count()
        count_image_files = 0
        for _, _, files in os.walk(product_image_media_path):
            count_image_files += len(files)
        self.assertEqual(count_image_files, product_image_objects_count)
