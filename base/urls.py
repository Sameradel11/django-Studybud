from django.urls import path
from . import views


urlpatterns = [

    path('',views.home,name="home"),

    path('room/<str:pk>',views.room,name="room"),

    path('room_form',views.createroom , name="room_form"),

    path('room_update/<str:pk>',views.updateroom , name="room_update"),
    path('room_delete/<str:pk>',views.deleteroom , name="room_delete"),




]

