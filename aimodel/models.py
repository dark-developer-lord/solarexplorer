from django.db import models

class ExoplanetPrediction(models.Model):
    MISSION_CHOICES = [
        ('kepler', 'Kepler'),
        ('tess', 'TESS'),
        ('k2', 'K2'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('error', 'Error'),
    ]
    
    # Убрали поле user
    mission = models.CharField(max_length=20, choices=MISSION_CHOICES)
    model_level = models.IntegerField(default=1)
    
    # Input data (храним как JSON)
    input_data = models.JSONField()
    
    # Prediction results
    planet_probability = models.FloatField()
    non_planet_probability = models.FloatField()
    
    # Model statistics
    confidence_level = models.CharField(max_length=20)
    prediction_status = models.CharField(max_length=20)
    recommendation = models.TextField()
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='success')
    
    # Добавим сессию для отслеживания анонимных пользователей
    session_key = models.CharField(max_length=40, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Exoplanet Prediction'
        verbose_name_plural = 'Exoplanet Predictions'
    
    def __str__(self):
        return f"{self.mission} - {self.planet_probability:.2%} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    def get_mission_display_name(self):
        return dict(self.MISSION_CHOICES).get(self.mission, self.mission.upper())
    
    def is_high_confidence(self):
        return self.confidence_level.lower() == 'высокая'
    
    def get_prediction_quality(self):
        if abs(self.planet_probability - 0.5) > 0.4:
            return "Excellent"
        elif abs(self.planet_probability - 0.5) > 0.25:
            return "Good"
        else:
            return "Uncertain"