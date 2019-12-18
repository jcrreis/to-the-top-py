
from django.urls import path, include
from .views import UserList

urlpatterns = [
  path('<int:user_id>/games', UserList.userGameEndpoint),
  path('', UserList.usersEndpoint , name = 'user-list'),
]


# path('register/',RegisterUserView.as_view(),name= 'user'),
    # path('users/', UserList.usersEndpoint , name = 'user-list'),
    # path('users/', ,
    # path('upvotes/games/<int:game_id>', UpvoteList.upvotesByGameEndpoint),
    # path('upvotes/', UpvoteList.allupvotes, name="upvotes-list"),
    # path('upvotes/users/<int:user_id>', UpvoteList.upvotesByUserEndpoint),
    # path('upvotes/users/<int:user_id>/games', UpvoteList.upvotesByUserGameEndpoint),