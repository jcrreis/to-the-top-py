from django.http import HttpResponse
from .models import Game, Upvote
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from tothetop.serializers import UserSerializer,GameSerializer,UpvoteSerializer
from django.utils.encoding import force_text
from rest_framework import status
from .serializers import UserSerializer, GameSerializer, UpvoteSerializer
from django.utils.encoding import force_text
from rest_framework import status
from django.core import serializers
from django.http import *
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated,AllowAny
import json





@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('users-list', request=request, format=format),
        'games': reverse('games-list', request=request, format=format),
        'upvotes': reverse('upvotes-list', request=request, format=format)
    })

# GAME ENDPOINTS


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
            print(data)
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


# UPVOTE ENDPOINTS


class UpvoteList(generics.ListAPIView):
    """
    List all upvotes of a game or upvote that game
    /upvotes/games/{game_id}
    """
    def upvotesByGameEndpoint(request,game_id):
        method = request.method
        if method == 'GET':
            upvotes = Upvote.objects.get(game=game_id)
            serializer = UpvoteSerializer(upvotes, many=True)
            return JsonResponse(serializer.data,safe = False)
        elif method == 'POST':
            data = JSONParser().parse(request)
            data['user'] = request.user.id
            serializer = UpvoteSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(GameSerializer(Game.objects.get(pk=data['game'])).data, status=201)
            return JsonResponse(serializer.errors, status=400)
        elif method == 'DELETE':
            if(request.user.id == None):
                print(request.user.id)
                return JsonResponse(data="User not logged in", status=401, safe=False)
            else:
                upvote = Upvote.objects.get(game=game_id,user=request.user.id)
                upvote.delete()
                return JsonResponse(data="",status=201,safe=False)
        return JsonResponse(data="Not found", status = 404, safe=False)

    """
        List all upvotes of a user
        /upvotes/users/{user_id}
    """
    def upvotesByUserEndpoint(request,user_id):
        method = request.method
        if method == 'GET':
            upvotes = Upvote.objects.filter(user=user_id)
            serializer = UpvoteSerializer(upvotes, many=True)
            return JsonResponse(serializer.data,safe = False)
    
    
    
    """ 
    List all upvotes
    """
    def allupvotes(request):
        upvotes = Upvote.objects.all()
        serializer = UpvoteSerializer(upvotes, many=True)
        return JsonResponse(serializer.data, safe=False)
        


# USER ENDPOINTS


class RegisterUserView(generics.CreateAPIView):
    model = get_user_model()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    
    
class UserList(generics.ListAPIView):
    
    """
    List all users, or create a new user

    /users/
    """
    @csrf_exempt
    def usersEndpoint(request):
        method = request.method

        if method == 'GET':
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return JsonResponse(serializer.data, safe=False)

        elif method == 'POST':
            data = JSONParser().parse(request)
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)

        else:
            HttpResponse(status=405)




    """
    Retrieve, delete or update a user

    /users/{user_id}/
    """
    
    def userEndpoint(request, user_id):
        method = request.method

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return HttpResponse(status=404)

        if method == 'GET':
            serializer = UserSerializer(user)
            return JsonResponse(serializer.data)

        elif method == 'PUT':
            data = JSONParser().parse(request)
            serializer = UserSerializer(user, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)

        elif method == 'DELETE':
            user.delete()
            return HttpResponse(status=204)

        # else:
            #print("estive aqui")
            # HttpResponse(status=405)
