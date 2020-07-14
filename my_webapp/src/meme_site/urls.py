from django.urls import path

from .views import (
    MemeListView,
    MemeAddView,
    UserMemeListView,
    MemeLobby,
    MemeDetailView,
    MemeDelete
)

urlpatterns = [
    path('', MemeListView.as_view(), name="memeListView"),
    path('lobby/', MemeLobby.as_view(), name='memeLobbyListView'),
    path('<int:pk>/', MemeDetailView.as_view(), name='memeDetailView'),
    path('user/<str:username>/', UserMemeListView.as_view(), name="userMemes"),
    path('<int:pk>/unlike/', MemeDetailView.as_view(), name="unlike-meme-detail"),
    path('<int:pk>/like/', MemeDetailView.as_view(), name="like-meme-detail"),
    path('<int:pk>/unlike/list', MemeListView.as_view(), name="unlike-meme"),
    path('<int:pk>/like/list', MemeListView.as_view(), name="like-meme"),
    path('add/', MemeAddView.as_view(), name="memeAdd"),
    path('<int:pk>/delete/', MemeDelete.as_view(), name='memeDeleteView')
]
