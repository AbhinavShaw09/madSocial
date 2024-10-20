from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, UserLoginForm, UserEditsForm


def signup_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  # Hash the password
            user.save()
            return redirect(
                "login"
            )  # Redirect to login page after successful registration
    else:
        form = UserRegistrationForm()
    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(
                    "list_post"
                )  # Redirect to home page after successful login
    else:
        form = UserLoginForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)  # Logout the user
    return redirect("login")  # Redirect to login page after logout


def user_details_view(request):
    user = request.user
    return render(request, "accounts/user_details.html", {"user": user})


def edit_profile_view(request):
    if request.method == "POST":
        form = UserEditsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("user_details")
            
    if request.method == 'GET':
        form = UserEditsForm(instance=request.user)
        return render(request, "accounts/edit_profile.html", {"form": form})
