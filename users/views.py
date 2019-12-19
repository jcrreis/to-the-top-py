from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django.utils.encoding import force_text
from rest_framework import status
from users.serializers import UserSerializer
from games.serializers import GameSerializer
from games.models import Game
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

class RegisterUserView(generics.CreateAPIView):
  model = get_user_model()
  permission_classes = (AllowAny,)
  serializer_class = UserSerializer
    
    
class UsersList(generics.ListAPIView):
  model = get_user_model()
  permission_classes = (AllowAny,)
  serializer_class = UserSerializer
  queryset = User.objects.all()

class UserList(generics.RetrieveAPIView):
  model = get_user_model()
  permission_classes = (AllowAny,)
  serializer_class = UserSerializer
  queryset = User.objects.all()


 
