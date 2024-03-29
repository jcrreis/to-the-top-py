from django.http import HttpResponse
from games.models import Game
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import GameSerializer
from rest_framework import status
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly,AllowAny
from games.permissions import IsOwnerOrReadOnly
from django.http import JsonResponse
import json


"""
/games/<int:pk>
"""
class GameEndpoint(generics.RetrieveUpdateDestroyAPIView):
  model = Game
  permission_classes = (IsOwnerOrReadOnly,)
  serializer_class = GameSerializer
  queryset = Game.objects.all()


"""
/games/

"""
class GamesEndpoint(generics.ListCreateAPIView):
  model = Game
  permission_classes = (IsAuthenticatedOrReadOnly,)
  serializer_class = GameSerializer
  queryset = Game.objects.all()

"""
/games/user/<int:pk>
"""
class UserGamesEndpoint(generics.ListAPIView):
  model = Game
  permission_classes = (IsAuthenticatedOrReadOnly,)
  serializer_class = GameSerializer
  def get_queryset(self):
    return Game.objects.filter(user=self.kwargs['pk'])

