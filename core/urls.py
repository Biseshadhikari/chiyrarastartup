from django.urls import path
from .views import *
urlpatterns = [
    path('',home,name = "home"),
    path("story/<str:slug>",storyDetail,name ="storyDetail"),
    path('login/',signin,name = "login"),
    path('register/',register,name = "register"),
    path('reply', replyPage, name='reply'),
    path('logout/', user_logout, name='logout'),
    path('aboutus/', aboutUs, name='aboutus'),


]
