from django.urls import path
from .views import *

urlpatterns = [
    path("login/", user_login_view, name="user_login"),
    path("signup/", user_signup_view, name="user_signup"),
    path("change-password/", change_password, name="change_password"),
    path("logout/", user_logout_view, name="user_logout"),
    path("", home_view, name="home_page"),
    path("post-list", user_post_list, name="post_list"),
    path("<int:id>", recipe_details, name="recipe_details"),
    path("post-list/<int:id>", edit_recipe_details, name="edit_recipe_details"),
]
