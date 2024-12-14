from django.db import models



class Product(models.Model):
    pass
class ProductImage(models.Model):
    pass
class Tag(models.Model):
    pass
class Category(models.Model):
    pass
class SubCategory(models.Model):
    pass
class Review(models.Model):
    pass
class Specification(models.Model):
    pass
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