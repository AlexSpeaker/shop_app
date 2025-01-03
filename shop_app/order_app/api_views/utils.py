from typing import List

from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import Q
from order_app.models import Basket
from order_app.models.order import Order
from rest_framework.request import Request


def merge_baskets(user: AbstractBaseUser, request: Request) -> None:
    """
    Функция слияния корзин.
    Когда пользователь проходит аутентификацию,
    выявит его анонимные корзины и объединит их с корзинами пользователя.

    :param user: Пользователь.
    :param request: Request.
    :return: None.
    """

    anonymous_user_id = request.session.get("anonymous_user_id", None)
    if not anonymous_user_id:
        return
    all_baskets = (
        Basket.objects.select_related("product")
        .filter((Q(user=user) | Q(session_id=anonymous_user_id)) & Q(order=None))
        .order_by("product__pk")
    )
    if not all_baskets.count():
        return
    baskets: List[Basket] = []
    for basket in all_baskets:
        if baskets and baskets[-1].product.pk == basket.product.pk:
            baskets[-1].count += basket.count
            baskets[-1].session_id = None
            baskets[-1].user = user
            basket.delete()
        else:
            basket.session_id = None
            basket.user = user
            baskets.append(basket)
    Basket.objects.bulk_update(baskets, ["count", "session_id", "user"])


def order_anonymous_to_user(user: AbstractBaseUser, request: Request) -> None:
    """
    Когда пользователь проходит аутентификацию,
    выявит его анонимный заказ и присвоит ему пользователя.

    :param user: Пользователь.
    :param request: Request.
    :return: None.
    """
    anonymous_user_id = request.session.get("anonymous_user_id", None)
    orders = Order.objects.filter(session_id=anonymous_user_id)
    if not orders.count():
        return
    for order in orders:
        order.user = user
        order.session_id = None
        order.full_name = user.profile.full_name
        order.email = user.profile.email
        order.phone = user.profile.phone
    Order.objects.bulk_update(
        orders, ["session_id", "user", "full_name", "email", "phone"]
    )
