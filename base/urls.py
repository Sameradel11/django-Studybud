from django.urls import path
from . import views


urlpatterns = [

    path('',views.home,name="home"),

    path('room/<str:pk>',views.room,name="room"),

    path('room_form',views.createroom , name="room_form"),

    path('login',views.loginpage,name='login'),

    path('logout',views.logoutpage,name='logout'),

    path('room_update/<str:pk>',views.updateroom , name="room_update"),

    path('room_delete/<str:pk>',views.deleteroom , name="room_delete"),

    path('register',views.register , name="register"),

    path('message_delete/<str:pk>',views.deletemessage , name="message_delete"),

    path('message_edit/<str:pk>',views.editmessage , name="message_edit"),

    path('profile/<str:pk>',views.profile,name='profile')







]

