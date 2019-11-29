from django.db import models
from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True

class Game(models.Model):
	name = models.CharField(max_length=200)
	price = models.FloatField(blank = True)
	description = models.CharField(max_length = 1000,blank = True)
	storeLink = models.URLField(max_length = 300,blank = True)
	trailerUrl = models.URLField(max_length = 300,blank = True)
	user = models.ForeignKey(User , on_delete = models.CASCADE)

	def __str__(self):
	 return self.name

	def getName(self):
		return self.name


class Upvote(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	user = models.ForeignKey(User , on_delete = models.CASCADE)
	class Meta:
		unique_together = [['user','game']]

