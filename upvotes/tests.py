from django.test import TestCase
from rest_framework.test import APITestCase, URLPatternsTestCase , APIClient
from users.models import User
from games.models import Game
from .models import Upvote
from faker import Factory
from django.urls import reverse
from rest_framework import status
from django.test import Client
import json


faker = Factory.create()


class UpvoteTests(APITestCase):

  def setUp(self):
   self.assertTrue(self.client.login(username='User', password='password')) 

  @classmethod
  def setUpTestData(cls):
    user = User.objects.create(username='User',  email=faker.ascii_free_email())
    user.set_password('password')
    user.save()
    assert User.objects.count() == 1
    data = {
        'name': faker.name(),
        'price':faker.pyfloat(positive = True),
        'description': faker.text(),
        'storeLink': faker.uri(),
        'trailerUrl':faker.uri()
    }
    c = Client()
    c.login(username='User', password='password')
    response = c.post('/games/',data,format='json')

  def test_get_create_and_delete_upvote(self):
    size = self.client.get('/games/').data
    id = size[0]['id']
    response = self.client.post('/upvotes/games/'+ str(id))
    self.assertEqual(response.status_code , status.HTTP_201_CREATED)
    response_dict = json.loads(response.content)
    self.assertEqual(response_dict['id'] , id)

    self.client.logout()

    response = self.client.post('/upvotes/games/'+ str(id))
    self.assertEqual(response.status_code , status.HTTP_403_FORBIDDEN)

    response = self.client.get('/upvotes/games/'+ str(id))
    self.assertEqual(response.status_code , status.HTTP_200_OK)

    response = self.client.delete('/upvotes/games/'+ str(id))
    self.assertEqual(response.status_code , status.HTTP_403_FORBIDDEN)

    self.assertTrue(self.client.login(username='User', password='password'))

    response = self.client.get('/upvotes/games/'+ str(id))
    self.assertEqual(response.status_code , status.HTTP_200_OK)

    response = self.client.delete('/upvotes/games/'+ str(id))
    self.assertEqual(response.status_code , status.HTTP_201_CREATED)

    response = self.client.get('/upvotes/games/'+ str(id))
    self.assertEqual(response.status_code , status.HTTP_200_OK)
    response_dict = json.loads(response.content)
    self.assertEqual(response_dict['upvotes'],0)
  

  def test_get_upvote_by_user(self):
    size = self.client.get('/games/').data
    id = size[0]['id']

    response = self.client.post('/upvotes/games/'+ str(id))
    self.assertEqual(response.status_code , status.HTTP_201_CREATED)

    response = self.client.get('/user/')
    url='/upvotes/users/'+str(response.data['pk'])

    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data),1)
  

  def test_get_upvote_by_user_with_game_details(self):
    size = self.client.get('/games/').data
    id = size[0]['id']
    response = self.client.post('/upvotes/games/'+ str(id))
    self.assertEqual(response.status_code , status.HTTP_201_CREATED)
    response = self.client.get('/user/')

    user = response.data['pk']
    url='/upvotes/users/'+str(user)+'/games'

    response = self.client.get(url)
    response_dict = json.loads(response.content)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response_dict[0]['id'],id)
    self.assertEqual(response_dict[0]['user'],user)
    self.assertEqual(len(response_dict),1)
  
  def test_get_all_uvpotes(self):
    size = self.client.get('/games/').data
    id = size[0]['id']
    
    response = self.client.post('/upvotes/games/'+ str(id))
    self.assertEqual(response.status_code , status.HTTP_201_CREATED)

    response = self.client.get('/upvotes/')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data),1)











    

  