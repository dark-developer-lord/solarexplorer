from django.contrib import admin
from .models import K2Model, KeplerModel, TESSModel, DF

@admin.register(K2Model)
class K2ModelAdmin(admin.ModelAdmin):
    list_display = ['pl_orbper', 'pl_rade', 'st_teff', 'st_rad']
    list_filter = ['st_teff']
    search_fields = ['pl_orbper']

@admin.register(KeplerModel)
class KeplerModelAdmin(admin.ModelAdmin):
    list_display = ['koi_period', 'koi_prad', 'koi_steff', 'koi_srad']
    list_filter = ['koi_steff']
    search_fields = ['koi_period']

@admin.register(TESSModel)
class TESSModelAdmin(admin.ModelAdmin):
    list_display = ['pl_orbper', 'pl_rade', 'st_teff', 'st_rad']
    list_filter = ['st_teff']
    search_fields = ['pl_orbper']

@admin.register(DF)
class DFAdmin(admin.ModelAdmin):
    list_display = ['mission', 'created_at', 'updated_at']
    list_filter = ['mission', 'created_at']
    readonly_fields = ['created_at', 'updated_at']