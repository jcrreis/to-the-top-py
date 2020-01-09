from users.models import User
from rest_framework import generics
from django.core import serializers
from users.serializers import UserSerializer
from games.serializers import GameSerializer
from games.models import Game
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework import status

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
  def perform_create(self,serializer):
    user = serializer.save()
    token = account_activation_token.make_token(user)
    message = render_to_string('email_confirm.html', {
                'user': user,
                'domain': 'to-the-top-ng.herokuapp.com',
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
    email = EmailMessage( "Activate your account" , message , to=[user.email] )
    email.send()

class ActivateUser(generics.GenericAPIView):
  def post(self, request, *args, **kwargs):
    try:
        uid = force_text(urlsafe_base64_decode(self.kwargs['uidb64']))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, self.kwargs['token']):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.',status = status.HTTP_200_OK)
    else:
        return HttpResponse('Activation link is invalid!',status = status.HTTP_400_BAD_REQUEST)
    
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


 
