from rest_framework import serializers
from .models import Upvote
from users.serializers import UserSerializer
from games.serializers import GameSerializer

class UpvoteSerializer(serializers.ModelSerializer):

  def create(self, validated_data):
    return Upvote.objects.create(**validated_data)

  class Meta:
    model = Upvote
    fields = ('game' , 'user')
