from django.urls import path
from product_app.api_views.catalog.catalog import CatalogAPIView
from product_app.api_views.catalog.categories import CategoryListView
from product_app.api_views.product.product import ProductView
from product_app.api_views.product.product_reviews import ProductReviewsView
from product_app.api_views.tags.tags import TagAPIView

app_name = "product_app"

urlpatterns = [
    path("categories", CategoryListView.as_view(), name="categories"),
    path("catalog", CatalogAPIView.as_view(), name="catalog"),
    path("tags", TagAPIView.as_view(), name="tags"),
    path("product/<int:product_id>", ProductView.as_view(), name="product"),
    path(
        "product/<int:product_id>/reviews",
        ProductReviewsView.as_view(),
        name="product-review",
    ),
]
