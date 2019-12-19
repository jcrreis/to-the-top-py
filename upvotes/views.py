from django.http import HttpResponse
from upvotes.models import Upvote
from games.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
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



class UpvoteListByGame(generics.GenericAPIView):
  """
  GET all game's upvotes or POST a new one

  /upvotes/games/<int:pk>
  """
  permission_classes = (IsAuthenticatedOrReadOnly,)
  def get(self, request, *args, **kwargs):
    upvotes = Upvote.objects.get(game=self.kwargs['pk'])
    serializer = UpvoteSerializer(upvotes, many=True)
    return JsonResponse(serializer.data,safe = False)

  def post(self, request, *args, **kwargs):
    data = {
      "game": self.kwargs['pk'],
      "user":request.user.id
    }
    serializer = UpvoteSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(GameSerializer(Game.objects.get(pk=self.kwargs['pk'])).data, status=201)
    else:
      #TODO error verification
      return JsonResponse(serializer.errors, status=409)




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

class UpvotesList(generics.ListAPIView):
  """
  GET all upvotes
  /upvotes
  """
  model = Upvote
  permission_classes = (AllowAny,)
  serializer_class = UpvoteSerializer
  queryset = Upvote.objects.all()

class DeleteOrRetrieveUserUpvote(generics.GenericAPIView):
  """
  Retrieve or delete a user upvote

  /upvotes/games/<int:game_id>/<int:user_id>
  """
  def get(self, request, *args, **kwargs):
    #TODO
    
  def delete(self, request, *args, **kwargs):
    if(request.user.id == None):
      print(request.user.id)
      return JsonResponse(data="User not logged in", status=401, safe=False)
    else:
      upvote = Upvote.objects.get(game=self.kwargs['pk'],user=request.user.id)
      upvote.delete()
      return JsonResponse(data="",status=201,safe=False)

    
