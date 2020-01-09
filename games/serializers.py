from rest_framework import serializers
from games.models import Game



class GameSerializer(serializers.ModelSerializer):
  upvotes = serializers.ReadOnlyField()
  image = serializers.ImageField(required = False)

  def create(self , validated_data):
    validated_data['user'] = self.context['request'].user
    
    return Game.objects.create(**validated_data)

  class Meta:
    model = Game
    fields = ('id','name','price','description','storeLink','trailerUrl','user','upvotes','image','comments')
    read_only_fields = ('user',)