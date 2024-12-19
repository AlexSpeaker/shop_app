from django.urls import path
from product_app.api_views.catalog.catalog import CatalogAPIView
from product_app.api_views.catalog.categories import CategoryListView

app_name = "product_app"

urlpatterns = [
    path("categories", CategoryListView.as_view(), name="categories"),
    path("catalog", CatalogAPIView.as_view(), name="catalog"),
]
