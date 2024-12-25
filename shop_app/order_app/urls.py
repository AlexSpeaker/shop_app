from django.urls import path
from order_app.api_views.basket.basket import BasketAPIView

app_name = "order_app"

urlpatterns = [
    path("basket", BasketAPIView.as_view(), name="basket"),
]
