from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('compare', views.compare, name='compare')
]
