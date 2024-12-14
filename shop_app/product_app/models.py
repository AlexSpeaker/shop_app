from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Tag(models.Model):
    name = models.CharField(_("name"), max_length=100, null=False, blank=False)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Tag({self.name})"


class Category(models.Model):
    name = models.CharField(
        _("name"), max_length=100, unique=True, null=False, blank=False
    )

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Category({self.name})"


class SubCategory(models.Model):
    name = models.CharField(
        _("name"), max_length=100, unique=True, null=False, blank=False
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"SubCategory({self.name})"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField(_("text"), null=False, blank=False)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    rate = models.IntegerField(_("rate"), null=False, blank=False)

    def __str__(self) -> str:
        return f"{self.text[:10]}..."

    def __repr__(self) -> str:
        return f"Review({self.text[:10]}...)"


class Product(models.Model):
    category = models.ForeignKey(
        SubCategory, on_delete=models.PROTECT, related_name="products"
    )
    price = models.DecimalField(
        _("price"), max_digits=10, decimal_places=2, null=True, blank=False
    )
    count = models.IntegerField(_("count"), default=0, null=False, blank=False)
    created_at = models.DateTimeField(
        _("created at"), auto_now_add=True, null=False, blank=False
    )
    updated_at = models.DateTimeField(
        _("updated at"), auto_now=True, null=False, blank=False
    )
    title = models.CharField(_("title"), max_length=500, null=False, blank=False)
    description = models.TextField(_("description"), null=False, blank=False)
    full_description = models.TextField(
        _("full description"), null=False, blank=False, default=description
    )
    free_delivery = models.BooleanField(
        _("free delivery"), default=False, null=False, blank=False
    )
    tags = models.ManyToManyField(Tag, verbose_name=_("tags"), related_name="products")

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return f"Product({self.title})"


class ProductImage(models.Model):
    title = models.CharField(_("title"), max_length=500, null=False, blank=False)
    image = models.ImageField(_("image"), null=False, blank=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return f"ProductImage({self.title})"


class Specification(models.Model):
    name = models.CharField(_("name"), max_length=500, null=False, blank=False)
    value = models.CharField(_("value"), max_length=500, null=False, blank=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="specifications"
    )

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Specification({self.name})"


# {
#   "id": 123,
#   "category": 55,
#   "price": 500.67,
#   "count": 12,
#   "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
#   "title": "video card",
#   "description": "description of the product",
#   "fullDescription": "full description of the product",
#   "freeDelivery": true,
#   "images": [
#     {
#       "src": "/3.png",
#       "alt": "Image alt string"
#     }
#   ],
#   "tags": [
#     "string"
#   ],
#   "reviews": [
#     {
#       "author": "Annoying Orange",
#       "email": "no-reply@mail.ru",
#       "text": "rewrewrwerewrwerwerewrwerwer",
#       "rate": 4,
#       "date": "2023-05-05 12:12"
#     }
#   ],
#   "specifications": [
#     {
#       "name": "Size",
#       "value": "XL"
#     }
#   ],
#   "rating": 4.6
# }
