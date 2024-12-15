from typing import TYPE_CHECKING

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from product_app.models import Category, SubCategory

if TYPE_CHECKING:

    ModelAdmin = admin.ModelAdmin[Category]
    TabularInline = admin.TabularInline[SubCategory, Category]
else:

    ModelAdmin = admin.ModelAdmin
    TabularInline = admin.TabularInline


class SubCategoryInline(TabularInline):
    """
    Инлайн класс для подкатегорий.
    """

    model = SubCategory
    can_delete = False
    verbose_name_plural = _("SubCategories")


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    """
    Класс админка для категорий.
    """

    inlines = (SubCategoryInline,)
    list_display = ("pk", "name")
    list_display_links = (
        "pk",
        "name",
    )
    search_fields = ("name",)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Category, Category]:
        """
        Подцепим подкатегории.

        :param request: HttpRequest.
        :return: QuerySet[Category, Category].
        """
        return super().get_queryset(request).prefetch_related("subcategories")
