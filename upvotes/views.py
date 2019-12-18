from django.http import HttpResponse
# from ..games.models import Game, Upvote
from upvotes.models import Upvote
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django.utils.encoding import force_text
from rest_framework import status
from .serializers import UpvoteSerializer
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
                return JsonResponse(GameSerializer(Game.objects.get(pk=game_id)).data,status=201,safe=False)
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
    
    def upvotesByUserGameEndpoint(request,user_id):
         method = request.method
         if method == 'GET':
          upvotes = Upvote.objects.filter(user=user_id)
          games = Game.objects.filter(id__in= upvotes.values('game'))
          serializer = GameSerializer(games, many=True)
          return JsonResponse(serializer.data, safe=False)
    

    """ 
    List all upvotes
    """
    def allupvotes(request):
        upvotes = Upvote.objects.all()
        serializer = UpvoteSerializer(upvotes, many=True)
        return JsonResponse(serializer.data, safe=False)
    
