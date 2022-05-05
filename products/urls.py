from django.urls    import path
from products.views import ProductDetailView,ProductSearchView,ProductListView

urlpatterns = [
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/search',ProductSearchView.as_view()),
    path('',ProductListView.as_view()),
]