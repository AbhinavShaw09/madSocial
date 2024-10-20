from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserLoginForm, UserEditsForm
from django.contrib.auth.decorators import login_required


def signup_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  
            user.save()
            return redirect(
                "login"
            )  
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
                ) 
    else:
        form = UserLoginForm()
    return render(request, "accounts/login.html", {"form": form})

@login_required 
def logout_view(request):
    logout(request) 
    return redirect("login")  


@login_required 
def edit_profile_view(request):
    if request.method == "POST":
        form = UserEditsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("user_details")
            
    if request.method == 'GET':
        form = UserEditsForm(instance=request.user)
        return render(request, "accounts/edit_profile.html", {"form": form})

@login_required 
def user_profile_view(request, id=None):
    if request.method == 'GET':
        if id == None:
             user = request.user
        else:
            user = get_object_or_404(User, id=id)
    return render(request,"accounts/user_details.html",{"user":user})
