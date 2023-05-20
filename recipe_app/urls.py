from django.urls import path
from .views import *

urlpatterns = [
    path("", home_view, name="home_page"),
    path("login/", user_login_view, name="user_login"),
    path("signup/", user_signup_view, name="user_signup"),
    path("<int:id>", recipe_details, name="recipe_details"),
    path("logout/", user_logout_view, name="user_logout"),
]
