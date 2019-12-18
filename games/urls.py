from django.urls import path, include
from .views import GameList, GameEndpoint

urlpatterns = [
  path('<int:pk>',GameEndpoint.as_view()),
  # path('<int:game_id>', GameList.gameEndpoint),
  path('', GameList.gamesEndpoint, name="games-list"),
]