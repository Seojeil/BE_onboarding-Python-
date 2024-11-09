from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegisterAPIView.as_view(), name="register"),
    path("signin/", views.SignInAPIView.as_view(), name="signin"),
]
