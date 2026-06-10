from django.urls import path, include
from .views import HomePageView
from accounts.views import SignUpView

urlpatterns = [
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", HomePageView.as_view(), name="home"),
]

