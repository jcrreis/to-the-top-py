from rest_framework import serializers
from .models import User
User._meta.get_field('email')._unique = True


class UserSerializer(serializers.ModelSerializer):

  image = serializers.ImageField(required = False)

  def create(self , validated_data):
    if 'image' not in validated_data:
      validated_data['image'] = None
    user = User.objects.create(
      username = validated_data['username'],
      email = validated_data['email'],
      image = validated_data['image']
    )
    user.set_password(validated_data['password'])
    user.is_active = False
    user.save()
    return user


  class Meta:
    model = User
    fields = ('id' , 'password' , 'username' , 'email', 'image')	