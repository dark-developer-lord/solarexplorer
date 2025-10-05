from django.urls import path
from .views import ReceiveMLDataView

urlpatterns = [
    path('receive-ml-data/', ReceiveMLDataView.as_view()),
    
]