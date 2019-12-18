from rest_framework import serializers
from django.contrib.auth.models import User
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
		fields = ('id' , 'password' , 'username' , 'email')	