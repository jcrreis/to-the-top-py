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
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from games.permissions import IsOwnerOrReadOnly
from django.http import JsonResponse
import json

class GameEndpoint(generics.RetrieveUpdateDestroyAPIView):
  model = Game
  permission_classes = (IsOwnerOrReadOnly,)
  serializer_class = GameSerializer
  queryset = Game.objects.all()


class GamesEndpoint(generics.ListCreateAPIView):
  model = Game
  permission_classes = (IsAuthenticatedOrReadOnly,)
  serializer_class = GameSerializer
  queryset = Game.objects.all()

