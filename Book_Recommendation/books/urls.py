from django.urls import path, include
from books import views

urlpatterns = [
    path('', views.index, name="index"),
]
