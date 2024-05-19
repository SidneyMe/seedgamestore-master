from django.urls import path
from .views import get_games, get_my_games

urlpatterns = [
    path('games', get_games, name="games"),
    path('my_games', get_my_games, name="my_games"),
]
