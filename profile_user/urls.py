from django.urls import path
from profile_user.views import profile_view, saved_articles_view, edit_profile_view

app_name = "profile"

urlpatterns = [
    path('', profile_view, name='profile'),
    path('edit/', edit_profile_view, name='edit'),
    path('saved/', saved_articles_view, name='saved'),
]