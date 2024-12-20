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


def get_simple_img_file() -> SimpleUploadedFile:
    """
    Функция возвращает файл картинки.

    :return: SimpleUploadedFile
    """
    files_for_test_dir = Path(__file__).parent / "files_for_test"
    valid_file_path = files_for_test_dir / "image.png"
    with open(valid_file_path, "rb") as valid_file:
        image_file = SimpleUploadedFile(
            name="image.png",
            content=valid_file.read(),
            content_type="image/png",
        )
    return image_file


def get_tag() -> Tag:
    """
    Функция создаёт и возвращает тег.

    :return: Tag.
    """
    tag: Tag = Tag.objects.create(name="".join(choices(ascii_letters, k=6)))
    return tag


def get_category() -> Category:
    """
    Функция создаёт и возвращает категорию.

    :return: Category
    """
    category: Category = Category.objects.create(
        name="".join(choices(ascii_letters, k=6))
    )
    return category


def get_sub_category(category: Category) -> SubCategory:
    """
    Функция создаёт и возвращает подкатегорию.

    :param category: Category.
    :return: SubCategory.
    """
    sub_category: SubCategory = SubCategory.objects.create(
        name="".join(choices(ascii_letters, k=6)), category=category
    )
    return sub_category


def get_simple_product(subcategory: SubCategory) -> Product:
    """
    Функция создаёт и возвращает простой продукт.

    :param subcategory: SubCategory.
    :return: Product.
    """
    product: Product = Product.objects.create(
        category=subcategory,
        title="".join(choices(ascii_letters, k=6)),
        price=100,
        count=100,
        description="".join(choices(ascii_letters, k=6)),
        full_description="".join(choices(ascii_letters, k=6)),
    )
    return product


def get_review(product: Product) -> Review:
    """
    Функция создаёт и возвращает отзыв на продукт.

    :param product: Product.
    :return: Review.
    """
    review: Review = Review.objects.create(
        product=product,
        author="".join(choices(ascii_letters, k=6)),
        email=f'{"".join(choices(ascii_letters, k=6))}@{"".join(choices(ascii_letters, k=6))}.com',
        text="".join(choices(ascii_letters, k=1000)),
        rate=randint(1, 5),
        date=now(),
    )
    return review


def get_specification(product: Product) -> Specification:
    """
    Функция создаёт и возвращает спецификацию продукта.

    :param product: Product.
    :return: Specification.
    """
    specification: Specification = Specification.objects.create(
        product=product,
        name="".join(choices(ascii_letters, k=6)),
        value="".join(choices(ascii_letters, k=6)),
    )
    return specification


def get_product_image(product: Product) -> ProductImage:
    """
    Функция создаёт и возвращает картинку продукта.

    :param product: Product.
    :return: ProductImage.
    """
    product_image: ProductImage = ProductImage.objects.create(
        product=product,
        image=get_simple_img_file(),
        title="".join(choices(ascii_letters, k=6)),
    )
    return product_image


def get_product() -> Product:
    """
    Создаём продукт со всеми связанными сущностями.

    :return: Product.
    """
    category = get_category()
    sub_category = get_sub_category(category)
    tag = get_tag()
    product = get_simple_product(sub_category)
    product.tags.add(tag)
    product.save()
    get_review(product)
    get_specification(product)
    get_product_image(product)

    return product
