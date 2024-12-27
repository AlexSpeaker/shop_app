from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    """
    Модель заказа.

    **created_at** Дата и время создания. \n
    **user** Пользователь прошедший аутентификацию. \n
    **session_id** ID анонимного пользователя. \n
    **full_name** ФИО пользователя. \n
    **email** Email пользователя. \n
    **phone** Phone пользователя. \n
    **delivery_type** Тип доставки. \n
    **payment_type** Тип оплаты. \n
    **status** Статус заказа. \n
    **city** Город доставки. \n
    **address** Адрес доставки. \n
    **paid_for** Оплачен ли заказ. \n
    """

    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders", null=True, default=None
    )
    session_id = models.CharField(null=True, default=None)
    full_name = models.CharField(_("full name"), null=True, default=None)
    email = models.EmailField(_("email"), max_length=254, default=None, null=True)
    phone = models.CharField(_("phone"), max_length=17, null=True, default=None)
    delivery_type = models.CharField(
        _("delivery type"), max_length=16, null=True, default=None
    )
    payment_type = models.CharField(
        _("payment type"), max_length=16, null=True, default=None
    )
    city = models.CharField(_("city"), max_length=16, null=True, default=None)
    address = models.CharField(_("address"), max_length=255, null=True, default=None)
    paid_for = models.BooleanField(_("paid for"), default=False)

    @property
    def status(self) -> str:
        """
        Получение статуса заказа.

        :return: Статус заказа.
        """
        return "Создан" if not self.paid_for else "Оплачен"
