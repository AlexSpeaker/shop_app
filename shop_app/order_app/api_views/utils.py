import uuid

from order_app.models import Basket
from product_app.models import Product
from rest_framework.request import Request


def get_basket(request: Request, product: Product, count: int) -> Basket:
    """
    Функция подготовит объект Basket для создания.

    :param request: Request.
    :param product: Связанный продукт.
    :param count: Необходимое количество.
    :return: Объект Basket для создания.
    """

    basket = Basket(product=product, count=count)
    if request.user.is_authenticated:
        basket.user = request.user
    elif not request.session.get("anonymous_session_id"):
        session_id = uuid.uuid4().hex
        request.session["anonymous_session_id"] = str(session_id)
        basket.session_id = session_id
    else:
        session_id = request.session["anonymous_session_id"]
        basket.session_id = session_id
    return basket
