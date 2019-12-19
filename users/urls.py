
from django.urls import path, include
from .views import UsersList, UserList

urlpatterns = [
  path('<int:pk>', UserList.as_view()),
  path('', UsersList.as_view() , name = 'user-list'),

]
