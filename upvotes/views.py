from django.http import HttpResponse
from upvotes.models import Upvote
from games.permissions import IsOwnerOrReadOnly
from users.models import User
from games.models import Game
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django.utils.encoding import force_text
from rest_framework import status
from upvotes.serializers import UpvoteSerializer
from django.utils.encoding import force_text
from rest_framework import status
from django.core import serializers
from django.http import *
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAuthenticatedOrReadOnly
from games.serializers import GameSerializer
import json
from django.db import IntegrityError
from games.permissions import IsOwnerOrReadOnly


class UpvoteListByGame(generics.GenericAPIView):
  """
  GET all game's upvotes or POST a new one

  /upvotes/games/<int:pk>
  """
  permission_classes = (IsAuthenticatedOrReadOnly,)

  def post(self, request, *args, **kwargs):
    data = {
      "game": self.kwargs['pk'],
      "user":request.user.id
    }
    serializer = UpvoteSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        gameSerializer = GameSerializer(Game.objects.get(pk=self.kwargs['pk']))
        if(gameSerializer.data['image'] != None):
          hostUrl = 'http://'+request.get_host()
          imgAbsolutePath = hostUrl+gameSerializer.data['image']
          gameSerializer._data['image'] = imgAbsolutePath
        return JsonResponse(gameSerializer.data, status=201)
    else:
      #TODO error verification
      return JsonResponse(serializer.errors, status=409)
    
  def get(self, request, *args, **kwargs):
    """
    TODO Get not found , 404 error
    """
    game = Game.objects.get(id=self.kwargs['pk'])
    serializer = GameSerializer(game)
    serializer.data['user'] = request.user.id
    return JsonResponse(serializer.data,status=200,safe=False)

  def delete(self, request, *args, **kwargs):
    upvote = Upvote.objects.get(game=self.kwargs['pk'],user=request.user.id)
    upvote.delete()
    game = Game.objects.get(id=self.kwargs['pk'])
    serializer = GameSerializer(game)
    if(serializer.data['image'] != None):
      hostUrl = 'http://'+request.get_host()
      imgAbsolutePath = hostUrl+serializer.data['image']
      serializer._data['image'] = imgAbsolutePath
    return JsonResponse(serializer.data,status=200,safe=False)




class UpvoteListByUser(generics.ListAPIView):
  """
  GET all upvotes of user
  /upvotes/users/<int:pk>
  """
  model = Upvote
  permission_classes = (AllowAny,)
  serializer_class = UpvoteSerializer
  def get_queryset(self):
    return Upvote.objects.filter(user=self.kwargs['pk'])

class UpvoteListByUserWithGameDetails(generics.GenericAPIView):
  """
  GET all upvotes of user
  /upvotes/users/<int:pk>/games
  """
  permission_classes = (IsOwnerOrReadOnly,)
  def get(self, request, *args, **kwargs):
    upvotes = Upvote.objects.filter(user=self.kwargs['pk'])
    games = Game.objects.filter(id__in= upvotes.values('game'))
    serializer = GameSerializer(games, many=True)
    return JsonResponse(serializer.data, safe=False)


class UpvotesList(generics.ListAPIView):
  """
  GET all upvotes
  /upvotes
  """
  model = Upvote
  permission_classes = (AllowAny,)
  serializer_class = UpvoteSerializer
  queryset = Upvote.objects.all()


    
