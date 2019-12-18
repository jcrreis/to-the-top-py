from django.db import models
from django.apps import apps
from django.contrib.auth.models import User

class Upvote(models.Model):
	game = models.ForeignKey('games.Game', on_delete=models.CASCADE)
	user = models.ForeignKey(User , on_delete = models.CASCADE)
	class Meta:
		unique_together = [['user','game']]