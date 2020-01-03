from django.test import TestCase
from rest_framework.test import APITestCase, URLPatternsTestCase , APIClient
from django.urls import reverse
from rest_framework import status
from users.models import User
from .models import Game
from faker import Factory
import base64
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
import io
from base64 import b64decode
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import tempfile
from PIL import Image


faker = Factory.create()

class GameTests ( APITestCase ):

  def setUp(self):
    self.assertTrue(self.client.login(username='User', password='password')) 

  @classmethod
  def setUpTestData(cls):
    user = User.objects.create(username='User',  email=faker.ascii_free_email())
    user.set_password('password')
    user.save()
    assert User.objects.count() == 1

    
  
  def create_game(self, data):
    url = reverse('games-listCreate')
   
    response = self.client.post(url,data,format='json')
    return response

  def generate_game_data(self):
    data = {
        'name': faker.name(),
        'price':faker.pyfloat(positive = True),
        'description': faker.text(),
        'storeLink': faker.uri(),
        'trailerUrl':faker.uri()
    }
    return data
    
  def test_create_game_without_image(self): 
    data = self.generate_game_data()
    response = self.create_game(data)

    self.assertEqual(response.status_code , status.HTTP_201_CREATED)
    self.assertEqual(Game.objects.count() ,1)
    game = Game.objects.get(name= data['name'])
    self.assertEqual(game.name, response.data['name'])
    self.assertEqual(game.price,response.data['price'])
    self.assertEqual(game.description, response.data['description'] )
    self.assertEqual(game.storeLink, response.data['storeLink'])
    self.assertEqual(game.trailerUrl, response.data['trailerUrl'])
    self.assertFalse(bool(game.image))
    self.assertEqual(game.upvotes() ,0)

  def test_create_game_with_only_required_fields(self):
    data = {
        'name': faker.name(),
        'price':faker.pyfloat(positive = True),
    }

    response = self.create_game(data)

    self.assertEqual(response.status_code , status.HTTP_201_CREATED)
    self.assertEqual(Game.objects.count() ,1)
    game = Game.objects.get(name=data['name'])
    self.assertEqual(game.name, response.data['name'])
    self.assertEqual(game.price, response.data['price'])
    self.assertEqual(game.description , '')
    self.assertEqual(game.storeLink , '')
    self.assertEqual(game.trailerUrl , '')
    self.assertEqual(game.upvotes() ,0)

  def test_create_game_with_image(self):
    url = reverse('games-listCreate')
    image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    file = tempfile.NamedTemporaryFile(suffix='.png')
    image.save(file)
    with open(file.name, 'rb') as image:
      data = {
        'name': faker.name(),
        'price':faker.pyfloat(positive = True),
        'image':image
      }
      response = self.client.post(url,data,format='multipart')
      self.assertEqual(response.status_code , status.HTTP_201_CREATED)

  
  def test_create_game_with_no_name(self):
    data = {
        'price':faker.pyfloat(positive = True),
        'description': faker.text(),
        'storeLink': faker.uri(),
        'trailerUrl':faker.uri()
    }
    response = self.create_game(data)

    self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)
    self.assertEqual(Game.objects.count() ,0)
  
  def test_create_game_with_no_price(self):
    data = {
        'name': faker.name(),
        'description': faker.text(),
        'storeLink': faker.uri(),
        'trailerUrl':faker.uri()
    }
    response = self.create_game(data)

    self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)
    self.assertEqual(Game.objects.count(),0)

  def test_list_games(self):
    url = reverse('games-listCreate')
    for x in range(2):
      data = self.generate_game_data()
      response = self.create_game(data)

    self.assertEqual(Game.objects.count() , 2 )
    
    response = self.client.get(url)

    self.assertEqual(response.status_code , status.HTTP_200_OK)
    self.assertEqual(len(response.data) , 2)

    self.client.logout()

    response = self.client.get(url)

    self.assertEqual(response.status_code , status.HTTP_200_OK)
    self.assertEqual(len(response.data) , 2)

  
  def test_retrieve_game(self):
    data = self.generate_game_data()
    self.create_game(data)
    self.client.logout()
    id = self.client.get('/games/').data[0]['id']
    response = self.client.get('/games/' + str(id))

    self.assertEqual(response.status_code , status.HTTP_200_OK)
    self.assertEqual(response.data['name'] , data['name'])

    response = self.client.get('/games/-1')

    self.assertEqual(response.status_code , status.HTTP_404_NOT_FOUND)

  def test_update_game(self):
    data = self.generate_game_data()
    self.create_game(data)
    id = self.client.get('/games/').data[0]['id']
    new_data = data
    new_data['name'] = "Changed Name" 

    response = self.client.put('/games/' + str(id), new_data ,format='json')

    self.assertEqual(response.status_code , status.HTTP_200_OK)
    self.assertEqual(response.data['name'] , new_data['name'])
    self.assertEqual(response.data['description'], data['description'])

    new_data['name'] = None
    response = self.client.put('/games/' + str(id), new_data ,format='json')
    self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)
    
    self.client.logout()
    response = self.client.put('/games/' + str(id), data ,format='json')
    self.assertEqual(response.status_code , status.HTTP_403_FORBIDDEN)

  def test_delete_game(self):
    for x in range(2):
      data = self.generate_game_data()
      self.create_game(data)

    response = self.client.get('/games/')
    id = response.data[0]['id']
    self.assertEqual(len(response.data) , 2)

    response = self.client.delete('/games/' + str(id))
    self.assertEqual(response.status_code ,status.HTTP_204_NO_CONTENT)
    size = self.client.get('/games/').data
    id = size[0]['id']
    self.assertEqual(len(size) , 1)

    self.client.logout()
    response = self.client.delete('/games/' + str(id))
    self.assertEqual(response.status_code ,status.HTTP_403_FORBIDDEN)
    size = self.client.get('/games/').data
    id = size[0]['id']
    self.assertEqual(len(size) , 1)

  def test_list_game_user(self):
    for x in range(2):
      data = self.generate_game_data()
      self.create_game(data)

    user_id = self.client.get('/user/').data['pk']

    response = self.client.get('/games/user/' + str(user_id))
    self.assertEqual(response.status_code , status.HTTP_200_OK)
    self.assertEqual(len(response.data), 2)

    self.client.logout()

    user = User.objects.create(username='Number Two',  email=faker.ascii_free_email())
    user.set_password('password')
    user.save()

    self.assertTrue(self.client.login(username='Number Two', password='password'))
    data = self.generate_game_data()
    self.create_game(data)

    response = self.client.get('/games/user/' + str(user_id))
    self.assertEqual(response.status_code , status.HTTP_200_OK)
    self.assertEqual(len(response.data), 2)



    
    







  
  