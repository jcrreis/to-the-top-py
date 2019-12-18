from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django.utils.encoding import force_text
from rest_framework import status
from  users.serializers import UserSerializer
from django.utils.encoding import force_text
from rest_framework import status
from django.core import serializers
from django.http import *
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated,AllowAny
import json

class RegisterUserView(generics.CreateAPIView):
    model = get_user_model()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    
    
class UserList(generics.ListAPIView):
    
    """
    List all users, or create a new user

    /users/
    """
    @csrf_exempt
    def usersEndpoint(request):
        method = request.method

        if method == 'GET':
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return JsonResponse(serializer.data, safe=False)

        elif method == 'POST':
            data = JSONParser().parse(request)
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)

        else:
            HttpResponse(status=405)




    """
    Retrieve, delete or update a user

    /users/{user_id}/
    """
    
    def userEndpoint(request, user_id):
        method = request.method

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return HttpResponse(status=404)

        if method == 'GET':
            serializer = UserSerializer(user)
            return JsonResponse(serializer.data)

        elif method == 'PUT':
            data = JSONParser().parse(request)
            serializer = UserSerializer(user, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)

        elif method == 'DELETE':
            user.delete()
            return HttpResponse(status=204)

        # else:
            #print("estive aqui")
            # HttpResponse(status=405)
    """
    /users/{user_id}/games
    """  
    def userGameEndpoint(request,user_id):
        method = request.method
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return HttpResponse(status=404)

        if method == 'GET':
            games = Game.objects.filter(user=user_id)
            serializer = GameSerializer(games, many=True)
            return JsonResponse(serializer.data, safe=False)

