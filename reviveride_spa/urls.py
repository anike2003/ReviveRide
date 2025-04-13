from django.urls import path
from . import views
# from .views import forgot_password, reset_password

urlpatterns = [
    path('login', views.Login,name='login'),
    path('logout', views.Logout,name='logout'),
    path('signup', views.Signup,name='signup'),
    path('create_new_password', views.Create_new_password,name='create_new_password'),
    path('forgot_password', views.Forgot_password,name='forgot_password'),
    path('dashboard', views.Dashboard,name='dashboard'),
    path('password_successful', views.Password_successful,name='password_successful'),
    path('createID', views.CreateID,name='createID'),
    path('feedback', views.Feedback,name='feedback'),
    path('chatbox', views.Chatbox,name='chatbox'),
    path('locationFinder', views.LocationFinder,name='locationFinder'),
    path('service', views.Service,name='service'),
    path('notification', views.Notification,name='notification'),
    path('payment', views.Payment,name='payment'),
  
   

    ]
