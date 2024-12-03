from django.urls import path

from . import views

urlpatterns = [

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("", views.index, name = "index"),
    path("new_trip", views.new_trip, name = "new_trip"),
    path("trip/<int:id>", views.trip, name = "trip"),
    path("new_activity/<int:id>", views.new_activity, name = "new_activity"),
    path("activity_details/<str:category>/<int:id>", views.activity_details, name = "activity_details"),
    path("edit_activity/<str:category>/<int:id>", views.edit_activity, name = "edit_activity"),
    path("edit_trip/<int:id>", views.edit_trip, name = "edit_trip"),
    
]