from django.urls import path
from .views import get_games, get_my_games, save_gamestate, load_gamestate

urlpatterns = [
    path('games', get_games, name="games"),
    path('my_games', get_my_games, name="my_games"),
    path('save', save_gamestate, name="save_gamestate"),
    path('load', load_gamestate, name="load_gamestate")
]
