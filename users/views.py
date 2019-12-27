from users.models import User
from rest_framework import generics
from django.core import serializers
from users.serializers import UserSerializer
from games.serializers import GameSerializer
from games.models import Game
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated,AllowAny

"""
/register/

Endpoint that registers a user with the given data , in the request body

Only Handles Posts Requests
"""
class RegisterUserView(generics.CreateAPIView):
  """
  Create new users
  /register
  """
  model = get_user_model()
  permission_classes = (AllowAny,)
  serializer_class = UserSerializer
    
"""
/users/

Endpoint that lists all registed users 

Only Handles Get Requests , used for listing a collection of models
"""
class UsersList(generics.ListAPIView):
  """
  List all users
  /users
  """
  model = get_user_model()
  permission_classes = (AllowAny,)
  serializer_class = UserSerializer
  queryset = User.objects.all()

"""  
/user/<int:pk>

Endpoint that lists the information of a given user with that id

Only Handles Get Requests, used for listing a single model of instance
"""

class UserList(generics.RetrieveAPIView):
  """
  Retrieve a user
  /users/<int:pk>
  """
  model = get_user_model()
  permission_classes = (AllowAny,)
  serializer_class = UserSerializer
  queryset = User.objects.all()


 
