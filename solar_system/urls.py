from django.urls import path
from . import views

urlpatterns = [
    path('galaxy/', views.galaxy, name='galaxy'),  # Пустой путь для главной страницы
]