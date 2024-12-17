from typing import TYPE_CHECKING, Optional

from auth_app.models import Profile
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:

    ModelAdmin = UserAdmin[User]
    StackedInline = admin.StackedInline[Profile, User]
else:

    ModelAdmin = UserAdmin
    StackedInline = admin.StackedInline


class ProfileInline(StackedInline):
    """
    Класс инлайн для профиля пользователя.
    """

    model = Profile
    can_delete = False
    verbose_name_plural = _("Profile")
    fields = "name", "patronymic", "surname", "phone", "email", "avatar"


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
    search_fields = (
        "username",
        "profile__name",
        "profile__surname",
        "profile__patronymic",
        "profile__email",
        "profile__phone",
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
