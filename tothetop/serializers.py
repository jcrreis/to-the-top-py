from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Game , Upvote
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
	def create(self , validated_data):
		user = get_user_model().objects.create(
			username = validated_data['username'],
			email = validated_data['email']
		)
		user.set_password(validated_data['password'])
		user.save()
		return user

	class Meta:
		model = User
		fields = ('password' , 'username' , 'email')	


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
		fields = ('game' , 'user')