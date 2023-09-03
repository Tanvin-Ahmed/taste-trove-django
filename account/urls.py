from django.urls import path
from .views import register, profile, user_login, user_logout

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("profile/", profile, name="profile"),
    path("logout/", user_logout, name="logout"),
]
