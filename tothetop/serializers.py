from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Game , Upvote


class UserSerializer(serializers.ModelSerializer):
	def create(self , validated_data):
		return User.objects.create(**validated_data)

	class Meta:
		model = User
		fields = ('id', 'password' , 'username' , 'email','is_superuser','user_permissions' )	


class GameSerializer(serializers.ModelSerializer):
	def create(self , validated_data):
		return Game.objects.create(**validated_data)
	
	class Meta:
		model = Game
		fields = ('id','name','price','description','storeLink','trailerUrl','user')
	

class UpvoteSerializer(serializers.ModelSerializer):
	def create(self, validated_data):
		return Upvote.objects.create(**validated_data)
	
	class Meta:
		model = Upvote
		fields = ('game_id' , 'user_id')