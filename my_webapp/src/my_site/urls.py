from django.urls import path
from django.contrib.auth import views as AuthView

from .views import (
    register,
    profile
)

urlpatterns = [
    path('register/', register, name="mySiteRegister_page"),
    path('login/', AuthView.LoginView.as_view(template_name='my_site/login.html'), name="mySiteLogin_page"),
    path('profile/<str:user>/', profile, name="mySiteProfile_page"),
    path('logout/', AuthView.LogoutView.as_view(template_name='my_site/logout.html'), name="mySiteLogout_page")
]
