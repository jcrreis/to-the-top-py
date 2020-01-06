from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse

from rest_framework import status
from .models import User
import tempfile
from django.test import Client
from base64 import b64decode
from django.core.files.base import ContentFile
from io import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from django.core.files import File


class UserCreateClass(APITestCase):
  
  @staticmethod
  def create_user(username,email,password):
    """
    Aux method to create user without image
    """
    c = Client()
    data = {
      'username': username,
      'email': email,
      'password': password,
    }
    response = c.post(reverse('register'),data,format='json')
    return response


  @staticmethod
  def create_user_with_image(username,email,password,image):
    """
    Aux method to create user with image
    """
    c = Client()
    data = {
      'username': username,
      'email': email,
      'password': password,
      'image': image,
    }
    response = c.post(reverse('register'),data,format='json')
    return response
  

class UserRegisterTestCase(APITestCase):

  def test_create_account_without_image(self):
    """
    Ensure we can create a new user account without an image
    """
    
    response = UserCreateClass.create_user('joao','joao@gmail.com','123')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(User.objects.count(),1)
    self.assertEqual(User.objects.get().username,'joao')
  
  def test_create_account_with_image(self):
    """
    Ensure we can create a new user account with an image
    """
    image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    file = tempfile.NamedTemporaryFile(suffix='.png')
    image.save(file)
    with open(file.name, 'rb') as data:
      response = UserCreateClass.create_user_with_image('joao','joao@gmail.com','123',data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(User.objects.count(),1)
    self.assertEqual(User.objects.get().username,'joao')
    self.assertEqual(1,1)
    
  
  def test_username_is_required(self):
    """
    Ensure we can't create a new account without an username
    """
    response = UserCreateClass.create_user('','joao@gmail.com','123')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(User.objects.count(),0)

  def test_username_is_unique(self):
    """
    Ensure we can't create 2 accounts with same username
    """
    response1 = UserCreateClass.create_user('joao','joao@gmail.com','123')
    response2 = UserCreateClass.create_user('joao','john@gmail.com','123')
    self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(User.objects.count(),1)
  
  def test_email_is_required(self):
    """
    Ensure we can't create a new account without an email
    """
    response = UserCreateClass.create_user('joao','','123')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(User.objects.count(),0)
  
  def test_email_is_unique(self):
    """
    Ensure we can't create 2 accounts with the same email
    """
    response1 = UserCreateClass.create_user('joao','joao@gmail.com','123')
    response2 = UserCreateClass.create_user('john','joao@gmail.com','123')
    self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(User.objects.count(),1)
  
  def test_password_is_required(self):
    """
    Ensure we can't create an account without password
    """
    response = UserCreateClass.create_user('joao','joao@gmail.com','')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(User.objects.count(),0)


class UserAuthTestCase(APITestCase):
  loginUrl = '/login/'
  userUrl = '/user/'
  logoutUrl = '/logout/'
  def setUp(self):
    self.user = User.objects.create_user('joao', 'joao@gmail.com', 'password123')
    self.user.save()

  def test_login_and_logout_is_working(self):
    """
    Ensure /login/,/logout/ and /user/ endpoints work correctly
    """
    data = {
      'username': 'joao',
      'password': 'password123',
    }
    response = self.client.post(self.loginUrl,data,format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response = self.client.get(self.userUrl)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['username'],'joao')
    self.assertEqual(response.data['email'],'joao@gmail.com')
    response = self.client.post(self.logoutUrl)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    

class UsersEndpointTestCase(APITestCase):

  url = '/users/'
  def test_user_endpoint(self):
    """
    Ensure when a user is created we can access data at /users/<int:pk>/ correctly
    """
    response = UserCreateClass.create_user('joao','joao@gmail.com','123')
    id = response.data['id']
    response = self.client.get(self.url+str(id))
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    data = response.data
    self.assertEqual(data['username'],'joao')
    self.assertEqual(data['email'],'joao@gmail.com')
    
  
  def test_users_endpoint(self):
    """
    Ensure we can access all users created on system at /users/
    """
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data),0)
    response = UserCreateClass.create_user('joao','joao@gmail.com','123')
    response = UserCreateClass.create_user('admin','admin@gmail.com','123')
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data),2)

    

    






  
  
