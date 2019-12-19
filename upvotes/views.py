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



class UpvoteListByGame(generics.ListCreateAPIView):
  """
  GET all game's upvotes or POST a new one

  /upvotes/games/<int:pk>
  """
  model = Upvote
  permission_classes = (IsAuthenticatedOrReadOnly,)
  serializer_class = UpvoteSerializer 
  def get_queryset(self):
    return Upvote.objects.filter(game=self.kwargs['pk'])

  def perform_create(self, serializer):
    user = self.request.user
    game = self.kwargs['pk']
    serializer.validated_data['user'] = user
    serializer.validated_data['game'] = Game.objects.get(id=game)
    serializer.save()
  
  def create(self, request, *args, **kwargs):
    try:
        return super(UpvoteListByGame, self).create(request, *args, **kwargs)
    except IntegrityError:
        return HttpResponse({'error: Upvote is already done'} , status = 409)
    serializer_class = UpvoteSerializer


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

class DeleteOrRetrieveUserUpvote(generics.RetrieveDestroyAPIView):
  """
  Retrieve or delete a user upvote

  /upvotes/games/<int:game_id>/<int:user_id>
  """
  model = Upvote
  permission_classes = (IsOwnerOrReadOnly,)
  serializer_class = UpvoteSerializer
  def get_object(self):
    return Upvote.objects.get(game=self.kwargs['game_id'],user=self.kwargs['user_id'])

    
