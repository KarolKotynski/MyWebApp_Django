from django.urls import path
from django.contrib.auth import views as authView

from .views import (
    home_page,
    about_me,
    register,
    profile
)

urlpatterns = [
    path('', home_page, name="home_page"),
    path('about/', about_me, name="about_page"),
    path('register/', register, name="mySiteRegister_page"),
    path('login/', authView.LoginView.as_view(template_name='my_site/login.html'), name="mySiteLogin_page"),
    path('profile/', profile, name="mySiteProfile_page"),
    path('logout/', authView.LogoutView.as_view(template_name='my_site/logout.html'), name="mySiteLogout_page")
]
