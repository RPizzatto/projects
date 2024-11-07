from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page>" , views.pages, name="pages"),
    path("new_page", views.new_page, name="new_page"),
    path("edit/<str:page>", views.edit, name="edit"),
    path("random_page", views.random_page, name="random_page"),
    path("search", views.search, name="search")
]

