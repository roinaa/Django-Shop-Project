from django.urls import path
from .views import (
    CategoryListView,
    ProductListView,
    ProductDetailView,
    SaleProductsView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    SearchResultsView,
)

urlpatterns = [
    path('', CategoryListView.as_view(), name='category_list'),
    path('category/<int:category_id>/', ProductListView.as_view(), name='product_list'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('sale/', SaleProductsView.as_view(), name='sale_products'),
    path('add/', ProductCreateView.as_view(), name='add_product'),
    path('product/<int:product_id>/update/', ProductUpdateView.as_view(), name='update_product'),
    path('product/<int:product_id>/delete/', ProductDeleteView.as_view(), name='delete_product'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
]