from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from account.forms import RegisterForm, LoginForm
from profile_user.models import UserProfile



#Decorators
def super_admin_required(view_func):
    from functools import wraps
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or (request.user.profile.role) != 'super_admin':
            return redirect('main:main')
        return view_func(request, *args, **kwargs)
    return _wrapped


def admin_or_super_required(view_func):
    from functools import wraps
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or (request.user.profile.role) not in ('super_admin', 'admin'):
            return redirect('main:main')
        return view_func(request, *args, **kwargs)
    return _wrapped


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


@login_required
@admin_or_super_required
def dashboard_view(request):
    users = User.objects.select_related('profile').all().order_by('id')
    users_data = []
    for u in users:
        profile, _ = UserProfile.objects.get_or_create(user=u)
        users_data.append({'user': u, 'profile': profile})
    return render(request, 'account/dashboard.html', {'users_data': users_data})


@login_required
@super_admin_required
def ban_user_view(request, user_id):
    if request.method == 'POST':
        target = get_object_or_404(User, id=user_id)
        if target != request.user:
            target.is_active = not target.is_active
            target.save(update_fields=['is_active'])
    return redirect('account:dashboard')


@login_required
@super_admin_required
def set_role_view(request, user_id):
    if request.method == 'POST':
        target = get_object_or_404(User, id=user_id)
        new_role = request.POST.get('role', 'user')
        if new_role in ('super_admin', 'admin', 'user') and target != request.user:
            profile, _ = UserProfile.objects.get_or_create(user=target)
            profile.role = new_role
            profile.save(update_fields=['role'])
    return redirect('account:dashboard')
