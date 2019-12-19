
from django.urls import path, include
from .views import UsersList, UserList

urlpatterns = [
  path('<int:pk>', UserList.as_view()),
  path('', UsersList.as_view() , name = 'user-list'),

]


# path('register/',RegisterUserView.as_view(),name= 'user'),
    # path('users/', UserList.usersEndpoint , name = 'user-list'),
    # path('users/', ,
    # path('upvotes/games/<int:game_id>', UpvoteList.upvotesByGameEndpoint),
    # path('upvotes/', UpvoteList.allupvotes, name="upvotes-list"),
    # path('upvotes/users/<int:user_id>', UpvoteList.upvotesByUserEndpoint),
    # path('upvotes/users/<int:user_id>/games', UpvoteList.upvotesByUserGameEndpoint),