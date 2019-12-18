from django.db import models
from django.apps import apps
from django.contrib.auth.models import User

class Upvote(models.Model):
	GameModel = apps.get_model('games', 'Game',False)
	game = models.ForeignKey('GameModel', on_delete=models.CASCADE)
	user = models.ForeignKey(User , on_delete = models.CASCADE)
	class Meta:
		unique_together = [['user','game']]