from django.urls import path, include
from .views import UpvoteListByGame,UpvotesList, UpvoteListByUser, DeleteOrRetrieveUserUpvote,UpvoteListByUserWithGameDetails


urlpatterns = [
  path('games/<int:pk>', UpvoteListByGame.as_view()),
  path('', UpvotesList.as_view(), name="upvotes-list"),
  path('users/<int:pk>',UpvoteListByUser.as_view()),
  path('games/<int:game_id>/<int:user_id>', DeleteOrRetrieveUserUpvote.as_view()),
  path('users/<int:pk>/games', UpvoteListByUserWithGameDetails.as_view())
]

