"""tothetop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.api_root),
    path('', include('rest_auth.urls')),
    path('authenticated',views.isAuthenticatedUser),
    path('admin/', admin.site.urls),
    path('register/',views.RegisterUserView.as_view(),name= 'user'),
    path('games/<int:game_id>', views.GameList.gameEndpoint),
    path('games/', views.GameList.gamesEndpoint, name="games-list"),
    path('users/', views.UserList.usersEndpoint , name = 'user-list'),
    path('upvotes/games/<int:game_id>', views.UpvoteList.upvotesByGameEndpoint),
    path('upvotes/', views.UpvoteList.allupvotes, name="upvotes-list"),

]
