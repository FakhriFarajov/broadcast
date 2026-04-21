from django.urls import path
from . import views

app_name = "article"

urlpatterns = [
    path('article/', views.article_view, name='article' ),
    path("create/", views.create_article, name='create'),
]