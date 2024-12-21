from django.urls import path
from product_app.api_views.catalog.catalog import CatalogAPIView
from product_app.api_views.catalog.categories import CategoryListView
from product_app.api_views.product.product import ProductViewSet
from product_app.api_views.tags.tags import TagAPIView

app_name = "product_app"

urlpatterns = [
    path("categories", CategoryListView.as_view(), name="categories"),
    path("catalog", CatalogAPIView.as_view(), name="catalog"),
    path("tags", TagAPIView.as_view(), name="tags"),
    path("product/<int:product_id>", ProductViewSet.as_view(), name="product"),
]
