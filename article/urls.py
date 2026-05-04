from django.urls import path
from . import views

app_name = "article"

urlpatterns = [
    path("<int:id>/", views.article_view, name="article_by_id"),
    path("<int:id>/edit/", views.edit_article, name="edit"),
    path("<int:id>/react/<str:reaction_type>/", views.react_article, name="react_article"),
    path("<int:id>/save/", views.save_article, name="save"),
    path("create/", views.create_article, name="create"),
    path("<int:id>/comment/", views.create_comment, name="create_comment"),
]