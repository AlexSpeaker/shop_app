from django.urls import path
from product_app.api_views.catalog.categories import CategoryListView

app_name = "product_app"

urlpatterns = [
    path("categories", CategoryListView.as_view(), name="categories"),
    # path("tags", TagsListView.as_view(), name="tags"),
]
