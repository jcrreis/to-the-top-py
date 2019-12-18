from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import GameList

path('/<int:game_id>', GameList.gameEndpoint),
path('/', GameList.gamesEndpoint, name="games-list"),