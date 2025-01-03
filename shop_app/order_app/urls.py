from django.urls import path
from order_app.api_views.basket.basket import BasketAPIView
from order_app.api_views.order.orders import OrderAPIView
from order_app.api_views.order.orders_id import OrderIdAPIView
from order_app.api_views.payment.payment import PaymentAPIView

app_name = "order_app"

urlpatterns = [
    path("basket", BasketAPIView.as_view(), name="basket"),
    path("orders", OrderAPIView.as_view(), name="order"),
    path("order/<int:order_id>", OrderIdAPIView.as_view(), name="order_id"),
    path("payment/<int:order_id>", PaymentAPIView.as_view(), name="payment"),
]
