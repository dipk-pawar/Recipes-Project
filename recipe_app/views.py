from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login
from .models import Recipe
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator


def home_view(request):
    recipes = Recipe.objects.select_related().all()
    return render(request, "home.html", context={"recipes": recipes})


def recipe_details(request, id):
    recipe = Recipe.objects.get(id=id)
    return render(request, "post_details.html", context={"recipe": recipe})


class UserPostAPIView(View):
    def get(self, request):
        user = request.user
        recipes = Recipe.objects.filter(posted_by=user)
        return render(request, "user_posts_list.html", context={"recipes": recipes})

    def post(self, request):
        user = request.user
        search_key = request.POST.get("search")
        recipes = Recipe.objects.filter(posted_by=user, title__contains=search_key)
        return render(request, "user_posts_list.html", context={"recipes": recipes})


@method_decorator(login_required, name="dispatch")
class UserPostGetandSaveAPIView(View):
    def get(self, request):
        return render(request, "create_post.html")

    def post(self, request):
        title = request.POST.get("title")
        image = request.FILES.get("new_image")
        description = request.POST.get("description")
        if image is None:
            messages.error(request, "Please fill the required fields")
            return redirect("/recipe_world/post-list")
        user = request.user
        recipe = Recipe.objects.create(
            title=title, image=image, description=description, posted_by=user
        )
        recipe.save()
        messages.success(request, "Recipe saved successfully")
        return redirect("/recipe_world/post-list")


@method_decorator(login_required, name="dispatch")
class UserPostDetailAPIView(View):
    def get(self, request, id):
        try:
            recipe = Recipe.objects.get(id=id)
        except Exception:
            messages.error(request, "Sorry, Recipe not found")
            return redirect("/recipe_world/post-list")
        return render(request, "edit_post.html", context={"recipe": recipe})

    def post(self, request, id):
        if request.POST.get("_method") == "PUT":
            recipe = Recipe.objects.get(id=id)
            title = request.POST.get("title")
            image = request.FILES.get("new_image")
            description = request.POST.get("description")
            if image is not None:
                recipe.image = image
            recipe.title = title
            recipe.description = description
            recipe.save()
            messages.success(request, "Recipe updated successfully")
        elif request.POST.get("_method") == "DELETE":
            if recipe := Recipe.objects.filter(id=id):
                recipe.delete()
                messages.success(request, "Recipe deleted successfully")
            else:
                messages.error(request, "Sorry, Recipe not found")
        return redirect("/recipe_world/post-list")


@login_required
def user_logout_view(request):
    logout(request)
    messages.success(request, "Logout successfully")
    return redirect("/recipe_world/login/")  # Redirect to the login page after logout


@login_required
def change_password(request):
    if request.method != "POST":
        return render(request, "change_password.html")
    current_password = request.POST.get("current_password")
    new_password = request.POST.get("new_password")
    confirm_new_password = request.POST.get("confirm_new_password")
    if (
        not current_password.strip()
        or not new_password.strip()
        or not confirm_new_password.strip()
    ):
        messages.error(request, "Please fill the required fields")
        return redirect("/recipe_world/change-password/")
    user = request.user
    if not user.check_password(current_password):
        messages.error(request, "Invalid current password")
        return redirect("/recipe_world/change-password/")
    if new_password != confirm_new_password:
        messages.error(request, "Sorry, new password didn't matched")
        return redirect("/recipe_world/change-password/")

    # Update the user's password
    user.set_password(new_password)
    user.save()

    # Update the session authentication hash
    update_session_auth_hash(request, user)
    logout(request)
    messages.success(request, "Password changes successfully, Please login again")
    return redirect("/recipe_world/login/")


# Create your views here.
def user_login_view(request):
    if request.method == "POST":
        user_name = request.POST.get("username")
        user_password = request.POST.get("password")

        if not user_name.strip() or not user_password.strip():
            messages.error(request, "Please fill the required fields")
            return redirect("/recipe_world/login/")

        if not User.objects.filter(username=user_name).exists():
            messages.error(request, "Sorry, user not found")
            return redirect("/recipe_world/login/")

        user = authenticate(username=user_name, password=user_password)
        if user is None:
            messages.error(request, "Sorry, invalid password")
            return redirect("/recipe_world/login/")
        else:
            login(request, user)
            return redirect("/recipe_world/post-list")

    return render(request, "login.html")


def user_signup_view(request):
    if request.method != "POST":
        return render(request, "register.html")
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    user_name = request.POST.get("username")
    email = request.POST.get("email")
    user_password = request.POST.get("password")

    if (
        not first_name.strip()
        or not last_name.strip()
        or not user_name.strip()
        or not email.strip()
        or not user_password.strip()
    ):
        messages.error(request, "Please fill the required fields")
        return redirect("/recipe_world/signup/")

    filter_user = User.objects.filter(Q(username=user_name) | Q(email=email))
    if filter_user.exists():
        messages.error(request, "Sorry, username or email is already exists")
        return redirect("/recipe_world/signup/")

    new_user = User.objects.create(
        first_name=first_name, last_name=last_name, username=user_name, email=email
    )
    new_user.set_password(user_password)
    new_user.save()
    messages.success(request, "User registered successfully")
    return redirect("/recipe_world/login/")
