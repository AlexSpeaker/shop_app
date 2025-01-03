from typing import TYPE_CHECKING

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from product_app.models import SubCategory

if TYPE_CHECKING:

    ModelAdmin = admin.ModelAdmin[SubCategory]

else:

    ModelAdmin = admin.ModelAdmin


@admin.register(SubCategory)
class SubCategoryAdmin(ModelAdmin):
    """
    Класс админка для подкатегорий.
    """

    list_display = ("pk", "name", "category__name")
    list_display_links = (
        "pk",
        "name",
    )
    search_fields = ("name", "category__name")

    def get_queryset(self, request: HttpRequest) -> QuerySet[SubCategory, SubCategory]:
        """
        Подцепим Category.

        :param request: HttpRequest.
        :return: QuerySet[SubCategory, SubCategory].
        """
        return super().get_queryset(request).select_related("category")
