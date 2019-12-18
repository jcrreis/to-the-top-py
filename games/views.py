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
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from django.http import JsonResponse
import json

class GameEndpoint(generics.RetrieveUpdateDestroyAPIView):
  model = Game
  permission_classes = (IsAuthenticatedOrReadOnly,)
  serializer_class = GameSerializer
  queryset = Game.objects.all()

  def put(self, request, pk):
    try:
      game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
      return HttpResponse(status=404)
    data = JSONParser().parse(request)
    data['user'] = request.user.id
    serializer = GameSerializer(game, data=data)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=400)


class GameList(generics.ListAPIView):
    """
    List all games or create a new game

    /games/
    """
    def gamesEndpoint(request):
        if request.method == 'GET':
            games = Game.objects.all()
            serializer = GameSerializer(games, many=True)
            return JsonResponse(serializer.data, safe=False)

        elif request.method == 'POST':
            data = JSONParser().parse(request)
            data['user'] = request.user.id
            "FALTA VERIFICAR SE O USER ESTA LOGADO AQUI"
            serializer = GameSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)

        else:
            HttpResponse(status=405)
