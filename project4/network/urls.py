
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name ="new_post"),
    path("profile/<str:user>", views.profile, name ="profile"),
    path("add_follow/<str:user>", views.Add_Follow, name="add_follow"),
    path("remove_follow/<str:user>", views.remove_follow, name="remove_follow"),
    path("following", views.following, name="following"),
    path("edit/<int:id>", views.Edit, name="edit"),
    path("add_like", views.add_like, name = "add_like"),
    path("remove_like", views.remove_like, name = "remove_like"),
    path("like_counter/<int:id>", views.like_counter, name = "like_counter"),
    path("all_posts", views.all_posts, name="all_posts"),

]
