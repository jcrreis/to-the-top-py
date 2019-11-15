from django.http import HttpResponse
from .models import Game , Upvote
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from tothetop.serializers import UserSerializer,GameSerializer,UpvoteSerializer
from django.utils.encoding import force_text
from rest_framework import status

class CustomValidation(APIException):
    status_code=status.HTTP_403_FORBIDDEN
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, status_code):
        if status_code is not None:self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_text(detail)}
        else: self.detail = {'detail': force_text(self.default_detail)}

def authe(request):
	print(request.user.is_authenticated)
	if(not request.user.is_authenticated):
		raise CustomValidation('Access denied','username', status_code=status.HTTP_403_FORBIDDEN)


def getGame(request, game_name):
	  output = Game.objects.filter(name = game_name)
	  return HttpResponse(output)


def upvoteGame(request , game_id , user_id):
	 authe(request)
	 game_id = Game.objects.get(id=game_id)
	 user_id = User.objects.get(id=user_id)
	 Upvote.objects.create(game = game_id , user = user_id)
	 return HttpResponse("Fixinho")



class GameList(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class UpvoteList(generics.ListAPIView):
	queryset = Upvote.objects.all()
	serializer_class = UpvoteSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



	