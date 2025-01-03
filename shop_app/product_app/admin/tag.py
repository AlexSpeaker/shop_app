from typing import TYPE_CHECKING

from django.contrib import admin
from product_app.models import Tag

if TYPE_CHECKING:

    ModelAdmin = admin.ModelAdmin[Tag]

else:

    ModelAdmin = admin.ModelAdmin


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    """
    Класс админка для тегов.
    """

    list_display = ("pk", "name")
    list_display_links = (
        "pk",
        "name",
    )
    search_fields = ("name",)
