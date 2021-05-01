from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bid/<int:pk>/", views.bid, name="bid"),
    path("category/<int:pk>/", views.category, name="category"),
    path("create/", views.create, name="create"),
    path("closed/<int:pk>/", views.closed, name="closed"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("add_comment/<int:pk>/", views.add_comment, name="add_comment"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register")
]
