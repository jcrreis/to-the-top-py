
from django.urls import path, include
from .views import UsersList, UserList , ActivateUser
urlpatterns = [
  path('<int:pk>', UserList.as_view()),
  path('', UsersList.as_view() , name = 'user-list'),
  path('activate/<str:uidb64>/<str:token>/',ActivateUser.as_view()),
]