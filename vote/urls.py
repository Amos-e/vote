from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("members", views.members),
    path("manage", views.manage_view),
    path("cast-vote", views.cast_vote),
    path("poll/<slug>", views.poll_view),
    path("poll/activate/<slug>", views.activate_poll),
    path("api", views.api_view),
]