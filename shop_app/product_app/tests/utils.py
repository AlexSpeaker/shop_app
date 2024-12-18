from pathlib import Path
from random import choices, randint
from string import ascii_letters

from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.timezone import now
from product_app.models import (
    Category,
    Product,
    ProductImage,
    Review,
    Specification,
    SubCategory,
    Tag,
)


def get_product() -> Product:
    """
    Создаём продукт со всеми связанными сущностями.

    :return: Product.
    """
    files_for_test_dir = Path(__file__).parent / "files_for_test"
    valid_file_path = files_for_test_dir / "image.png"
    with open(valid_file_path, "rb") as valid_file:
        image_file = SimpleUploadedFile(
            name="image.png",
            content=valid_file.read(),
            content_type="image/png",
        )
    tag = Tag.objects.create(name="".join(choices(ascii_letters, k=6)))
    category = Category.objects.create(name="".join(choices(ascii_letters, k=6)))
    subcategory = SubCategory.objects.create(
        name="".join(choices(ascii_letters, k=6)), category=category
    )
    product: Product = Product.objects.create(
        category=subcategory,
        title="".join(choices(ascii_letters, k=6)),
        price=100,
        count=100,
        description="".join(choices(ascii_letters, k=6)),
        full_description="".join(choices(ascii_letters, k=6)),
    )
    product.tags.add(tag)
    product.save()
    Review.objects.create(
        product=product,
        author="".join(choices(ascii_letters, k=6)),
        email=f'{"".join(choices(ascii_letters, k=6))}@{"".join(choices(ascii_letters, k=6))}.com',
        text="".join(choices(ascii_letters, k=1000)),
        rate=randint(1, 5),
        date=now(),
    )
    Specification.objects.create(
        product=product,
        name="".join(choices(ascii_letters, k=6)),
        value="".join(choices(ascii_letters, k=6)),
    )
    ProductImage.objects.create(
        product=product,
        image=image_file,
        title="".join(choices(ascii_letters, k=6)),
    )
    return product
