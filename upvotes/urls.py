from django.urls import path, include
from .views import UpvoteList

urlpatterns = [
  path('games/<int:game_id>', UpvoteList.upvotesByGameEndpoint),
  path('', UpvoteList.allupvotes, name="upvotes-list"),
  path('users/<int:user_id>',UpvoteList.upvotesByUserEndpoint),
  path('users/<int:user_id>/games', UpvoteList.upvotesByUserGameEndpoint),
]

