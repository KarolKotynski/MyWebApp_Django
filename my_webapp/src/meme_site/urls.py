from django.urls import path

from .views import (
    MemeListView,
    #meme_detail_view,
    MemeLikeDown,
    MemeLikeUp,
    MemeAddView,
    UserMemeListView,
    delete_meme,
    MemeLobby,
    MemeDetailView,
)

urlpatterns = [
    path('', MemeListView.as_view(), name="memeListView"),
    path('lobby/', MemeLobby.as_view(), name='memeLobbyListView'),
    #path('<int:id>/', meme_detail_view, name="memeDetailView"),
    path('<int:pk>/', MemeDetailView.as_view(), name='memeDetailView'),
    path('user/<str:username>/', UserMemeListView.as_view(), name="userMemes"),
    path('<int:pk>/delete/', delete_meme, name='memeDeleteView'),
    path('<int:pk>/unlike/', MemeLikeDown.as_view(), name="like_down"),
    path('<int:pk>/like/', MemeLikeUp.as_view(), name="like_up"),
    path('add/', MemeAddView.as_view(), name="memeAdd")
]
