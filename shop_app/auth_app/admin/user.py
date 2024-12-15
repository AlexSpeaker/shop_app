from typing import TYPE_CHECKING, Optional

from auth_app.models import Profile
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from django.contrib.admin import StackedInline as _StackedInline
    from django.contrib.auth.admin import UserAdmin as _UserAdmin

    ModelAdmin = _UserAdmin[User]
    StackedInline = _StackedInline[Profile, User]
else:
    from django.contrib.auth.admin import UserAdmin

    ModelAdmin = UserAdmin
    StackedInline = admin.StackedInline


class ProfileInline(StackedInline):
    """
    Класс инлайн для профиля пользователя.
    """

    model = Profile
    can_delete = False
    verbose_name_plural = _("Profile")


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(ModelAdmin):
    """
    Класс админка для пользователя.
    """

    inlines = (ProfileInline,)
    list_display = (
        "pk",
        "username",
        "full_name",
        "last_login",
        "is_staff",
        "is_superuser",
    )
    list_display_links = (
        "pk",
        "username",
    )

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Permissions"),
            {
                "classes": ("collapse",),
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important dates"),
            {"classes": ("collapse",), "fields": ("last_login", "date_joined")},
        ),
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