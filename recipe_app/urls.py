from django.urls import path
from .views import *

urlpatterns = [
    path("", home_view, name="home_page"),
    path("<int:id>", recipe_details, name="recipe_details"),
    path("login/", user_login_view, name="user_login"),
    path("signup/", user_signup_view, name="user_signup"),
    path("change-password/", change_password, name="change_password"),
    path("logout/", user_logout_view, name="user_logout"),
    path("post-list", UserPostAPIView.as_view(), name="post_list"),
    path(
        "post-list/<int:id>",
        UserPostDetailAPIView.as_view(),
        name="edit_recipe_details",
    ),
    path(
        "get-or-create", UserPostGetandSaveAPIView.as_view(), name="get_or_create_post"
    ),
    path(
        "get-or-create", UserPostGetandSaveAPIView.as_view(), name="get_or_create_post"
    ),
]
