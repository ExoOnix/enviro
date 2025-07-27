from . import views
from django.urls import path

urlpatterns = [
    path('environment/<int:number>/', views.waiting_room, name='waiting_room'),
    path('', views.loading_room, name='loading_room'),
]
