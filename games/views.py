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
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.http import JsonResponse
import json

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

    """
    Retrive, update or delete a game

    /games/{game_id}/
    """

    def gameEndpoint(request, game_id):
        try:
            game = Game.objects.get(pk=game_id)
        except Game.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':
            serializer = GameSerializer(game)
            return JsonResponse(serializer.data)

        elif request.method == 'PUT':
            data = JSONParser().parse(request)
            data['user'] = request.user.id
            serializer = GameSerializer(game, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)

        elif request.method == 'DELETE':
            user_requester = request.user.id  # id do user que faz o pedido
            user_game = game.user.id  # id do user que publicou o jogo no site
            if(user_requester == user_game):
                game.delete()
                return HttpResponse(status=204)
            else:
                return HttpResponse(status=403)

        else:
            HttpResponse(status=405)
