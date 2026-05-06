from django.urls import path

from account.views import (
    register_view, register_success_view, login_view, logout_view,
    dashboard_view, ban_user_view, set_role_view,
)

app_name = "account"

urlpatterns = [
    path('register/', register_view, name='register'),
    path('register/success/', register_success_view, name='register_success'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboard/ban/<int:user_id>/', ban_user_view, name='ban_user'),
    path('dashboard/role/<int:user_id>/', set_role_view, name='set_role'),
]