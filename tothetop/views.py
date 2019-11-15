from django.http import HttpResponse
from .models import Game , Upvote
from django.contrib.auth.models import User
from rest_framework import generics
from tothetop.serializers import UserSerializer,GameSerializer,UpvoteSerializer

def getGame(request, game_name):
	  output = Game.objects.filter(name = game_name)
	  return HttpResponse(output)


def upvoteGame(request , game_id , user_id):
	 game_id = Game.objects.get(game_id)
	 user_id = User.objects.get(user_id)
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