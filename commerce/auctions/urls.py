from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("filetered_categories", views.display_category, name="display_category"),
    path("new_bid/<int:listing_id>", views.new_bid, name="new_bid"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("add_watchlist/<int:listing_id>", views.add_watchlist, name="add_watchlist"), 
    path("remove_watchlist/<int:listing_id>", views.remove_watchlist, name="remove_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("close_auction/<int:listing_id>", views.close_auction, name="close_auction"),
    path("closed_listing", views.closed_listing, name="closed_listing")

]
