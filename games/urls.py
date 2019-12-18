from django.urls import path, include
from .views import GameList

urlpatterns = [
  path('<int:game_id>', GameList.gameEndpoint),
  path('', GameList.gamesEndpoint, name="games-list"),
]