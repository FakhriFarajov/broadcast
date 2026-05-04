from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from account.forms import RegisterForm, LoginForm


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"]
            )
            request.session["registered_user"] = form.cleaned_data["username"]
            return redirect("account:register_success")
    else:
        form = RegisterForm()
    return render(request, "account/register.html", {"form": form})

def register_success_view(request):
    return render(request, "account/register_success.html", {
        "username": request.session.get('registered_user', "New User")
    })

def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )
            if user is not None:
                login(request, user)
                if next_url:
                    return redirect(next_url)
                return redirect("profile:profile")
            form.add_error(None, "Incorrect username or password")
    else:
        form = LoginForm()
    return render(request, "account/login.html", {"form": form, "next": next_url})

def logout_view(request):
    from django.contrib.auth import logout as auth_logout
    auth_logout(request)
    return redirect("account:login")