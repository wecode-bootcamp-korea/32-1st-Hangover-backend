from django.urls import path,include
from . import views

urlpatterns = [
    path('/search',views.ProductSearchView.as_view()),
]
