from django.urls import path

from users.views import SignUpView, SignInView, CartView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/carts', CartView.as_view())
]