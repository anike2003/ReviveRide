from django.urls import path
from . import views
# from .views import forgot_password, reset_password

urlpatterns = [
    path('login', views.login,name='login'),
    path('signup', views.signup,name='signup'),
    path('create_new_password', views.Create_new_password,name='create_new_password'),
    path('dashboard', views.Dashboard,name='dashboard'),
    path('password_successful', views.Password_successful,name='password_successful'),
   

    ]