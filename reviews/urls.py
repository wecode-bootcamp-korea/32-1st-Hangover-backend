from django.urls import path

from reviews.views import ReviewView, ReviewLikeView

urlpatterns = [
    path('', ReviewView.as_view()),
    path('/likes', ReviewLikeView.as_view())
]