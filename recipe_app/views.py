from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login
from .models import Recipe
from django.contrib.auth import logout


def home_view(request):
    recipes = Recipe.objects.select_related().all()
    return render(request, "home.html", context={"recipes": recipes})


def recipe_details(request, id):
    recipe = Recipe.objects.get(id=id)
    return render(request, "post_details.html", context={"recipe": recipe})


def user_logout_view(request):
    logout(request)
    messages.success(request, "Logout successfully")
    return redirect("/recipe_world/login/")  # Redirect to the login page after logout


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
            return redirect("/recipe_world/")

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
