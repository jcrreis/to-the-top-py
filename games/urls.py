from django.urls import path, include
from .views import GamesEndpoint, GameEndpoint, UserGamesEndpoint

urlpatterns = [
  path('<int:pk>',GameEndpoint.as_view()),
  path('', GamesEndpoint.as_view(), name="games-list"),
  path('user/<int:pk>',UserGamesEndpoint.as_view())
]