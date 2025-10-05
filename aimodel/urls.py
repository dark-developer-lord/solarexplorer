from django.urls import path
from . import views

urlpatterns = [
    # Exoplanet prediction pages
    path('exoplanet-predictor/', views.exoplanet_predictor, name='exoplanet_predictor'),
    # path('prediction-history/', views.prediction_history, name='prediction_history'),
    # path('prediction/<int:prediction_id>/', views.prediction_detail, name='prediction_detail'),
    
    # API endpoints
    path('api/predict-exoplanet/', views.predict_exoplanet_api, name='predict_exoplanet_api'),
]