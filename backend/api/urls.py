from django.urls import path

from .views import hello_world

urlpatterns = [
    path('parts/', hello_world, name='part-list'),
]
