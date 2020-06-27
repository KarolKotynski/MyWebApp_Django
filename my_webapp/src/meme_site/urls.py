from django.urls import path

from .views import (
    MemeListView,
    memeDetailView,
    Meme_like_up,
    Like_down,
    MemeAddView,
    UserMemeListView,
    deleteMeme,
    MemeLobby,
)

urlpatterns = [
    path('', MemeListView.as_view(), name="memeListView"),
    path('lobby/', MemeLobby.as_view(), name='memeLobbyListView'),
    path('<int:id>/', memeDetailView, name="memeDetailView"),
    path('user/<str:username>/', UserMemeListView.as_view(), name="userMemes"),
    path('<int:id>/delete/', deleteMeme, name='memeDeleteView'),
    path('<int:id>/like/', Meme_like_up.as_view(), name="like_up"),
    path('<int:id>/unlike/', Like_down.as_view(), name="like_down"),
    path('add/', MemeAddView.as_view(), name="memeAdd")
]
