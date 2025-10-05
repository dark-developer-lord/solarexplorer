from django.contrib import admin
from .models import ExoplanetPrediction

@admin.register(ExoplanetPrediction)
class ExoplanetPredictionAdmin(admin.ModelAdmin):
    list_display = ['id', 'mission', 'planet_probability', 'confidence_level', 'created_at', 'status']
    list_filter = ['mission', 'confidence_level', 'status', 'created_at']
    search_fields = ['mission', 'recommendation', 'prediction_status']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('mission', 'model_level', 'status')
        }),
        ('Input Data', {
            'fields': ('input_data',)
        }),
        ('Prediction Results', {
            'fields': ('planet_probability', 'non_planet_probability')
        }),
        ('Model Statistics', {
            'fields': ('confidence_level', 'prediction_status', 'recommendation')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'session_key')
        }),
    )
    
    # Добавим методы для отображения дополнительной информации
    def get_mission_display(self, obj):
        return obj.get_mission_display_name()
    get_mission_display.short_description = 'Mission'
    
    def prediction_quality(self, obj):
        return obj.get_prediction_quality()
    prediction_quality.short_description = 'Quality'