from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    # path("sign-up", views.SignUpView, name="sign-up"),
    path("sign-in/", views.SignInView, name="sign-in"),
    path("sign-out/", views.SignOutView, name="sign-out"),
]