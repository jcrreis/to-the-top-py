from django.db import models
from users.models import User
from upvotes.models import Upvote

class Game(models.Model):

    
  def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 10.0
    if filesize > megabyte_limit*1024*1024:
      raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

  name = models.CharField(max_length=200)
  price = models.FloatField()
  description = models.CharField(max_length = 1000,blank = True)
  storeLink = models.URLField(max_length = 300,blank = True)
  trailerUrl = models.URLField(max_length = 300,blank = True)
  user = models.ForeignKey(User , on_delete = models.CASCADE)
  image = models.ImageField(upload_to='games',null=True, blank=True, validators=[validate_image])

  def __str__(self):
    return self.name

  def getName(self):
    return self.name

  def upvotes(self):
    return Upvote.objects.filter(game=self.id).count()


