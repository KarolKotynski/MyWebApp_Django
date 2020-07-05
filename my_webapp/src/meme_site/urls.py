from django.urls import path

from .views import (
    MemeListView,
    meme_detail_view,
    MemeLikeDown,
    MemeLikeUp,
    MemeAddView,
    UserMemeListView,
    delete_meme,
    MemeLobby,
)

urlpatterns = [
    path('', MemeListView.as_view(), name="memeListView"),
    path('lobby/', MemeLobby.as_view(), name='memeLobbyListView'),
    path('<int:id>/', meme_detail_view, name="memeDetailView"),
    path('user/<str:username>/', UserMemeListView.as_view(), name="userMemes"),
    path('<int:id>/delete/', delete_meme, name='memeDeleteView'),
    path('<int:id>/unlike/', MemeLikeDown.as_view(), name="like_down"),
    path('<int:id>/like/', MemeLikeUp.as_view(), name="like_up"),
    path('add/', MemeAddView.as_view(), name="memeAdd")
]
