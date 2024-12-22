from django.urls import path
from product_app.api_views.catalog.banners import CatalogBannersAPIView
from product_app.api_views.catalog.catalog import CatalogAPIView
from product_app.api_views.catalog.categories import CategoryListAPIView
from product_app.api_views.catalog.limited import CatalogLimitedAPIView
from product_app.api_views.catalog.popular import CatalogPopularAPIView
from product_app.api_views.catalog.sales import CatalogSalesAPIView
from product_app.api_views.product.product import ProductView
from product_app.api_views.product.product_reviews import ProductReviewsView
from product_app.api_views.tags.tags import TagAPIView

app_name = "product_app"

urlpatterns = [
    path("categories", CategoryListAPIView.as_view(), name="categories"),
    path("catalog", CatalogAPIView.as_view(), name="catalog"),
    path("tags", TagAPIView.as_view(), name="tags"),
    path("products/popular", CatalogPopularAPIView.as_view(), name="product-popular"),
    path("products/limited", CatalogLimitedAPIView.as_view(), name="product-limited"),
    path("banners", CatalogBannersAPIView.as_view(), name="banners"),
    path("sales", CatalogSalesAPIView.as_view(), name="sales"),
    path("product/<int:product_id>", ProductView.as_view(), name="product"),
    path(
        "product/<int:product_id>/reviews",
        ProductReviewsView.as_view(),
        name="product-review",
    ),
]
