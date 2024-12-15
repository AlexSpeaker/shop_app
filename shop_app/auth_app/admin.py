from typing import TYPE_CHECKING, Optional

from auth_app.models import Profile
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest


if TYPE_CHECKING:
    from django.contrib.admin import ModelAdmin as _ModelAdmin
    from django.contrib.admin import StackedInline as _StackedInline

    ModelAdmin = _ModelAdmin[User]
    StackedInline = _StackedInline[Profile, User]
else:
    ModelAdmin = admin.ModelAdmin
    StackedInline = admin.StackedInline

admin.site.unregister(User)

class ProfileInline(StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"


@admin.register(User)
class UserAdmin(ModelAdmin):

    inlines = (ProfileInline,)
    list_display = ("pk", "username", "full_name", "last_login")
    list_display_links = (
        "pk",
        "username",
    )

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    @staticmethod
    def full_name(obj: User) -> Optional[str]:
        """
        Функция вернёт ФИО пользователя.
        :param obj: Объект пользователя.
        :return: ФИО пользователя, если профиль существует, иначе None.
        """
        return obj.profile.full_name if hasattr(obj, "profile") else None

    def get_queryset(self, request: HttpRequest) -> QuerySet[User, User]:
        """
        Функция подцепит профиль пользователя.
        
        :param request: HttpRequest.
        :return: QuerySet.
        """
        return super().get_queryset(request).select_related("profile")
