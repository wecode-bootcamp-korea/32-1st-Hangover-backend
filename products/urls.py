from django.urls    import path,include
from products.views import ProductDetailView,ProductSearchView

urlpatterns = [
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/search',ProductSearchView.as_view()),
]
