from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('add/', views.add_skill, name='add_skill'),
    path('logout/', views.logout_user, name='logout'),
    path('chatbot/', views.chatbot, name='chatbot'),
]