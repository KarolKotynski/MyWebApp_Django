from django.urls import path

from .views import (
    MemeListView,
    MemeLikeDown,
    MemeLikeUp,
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
    path('<int:pk>/delete/', MemeDelete.as_view(), name='memeDeleteView'),
    path('<int:pk>/unlike/', MemeLikeDown.as_view(), name="like_down"),
    path('<int:pk>/like/', MemeLikeUp.as_view(), name="like_up"),
    path('add/', MemeAddView.as_view(), name="memeAdd")
]
