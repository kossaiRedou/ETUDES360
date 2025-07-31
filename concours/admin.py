from django.contrib import admin
from .models import Concours

# Register your models here.

@admin.register(Concours)
class ConcoursAdmin(admin.ModelAdmin):
    list_display = ['titre', 'categorie', 'niveau', 'deadline', 'statut', 'actif']
    search_fields = ['titre', 'description', 'organisme']
    list_filter = ['categorie', 'niveau', 'statut', 'actif', 'deadline']
    date_hierarchy = 'deadline'
    readonly_fields = ['date_creation', 'date_modification']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('titre', 'description', 'categorie', 'niveau')
        }),
        ('Détails du concours', {
            'fields': ('deadline', 'localisation', 'region', 'nombre_places', 'prerequis', 'statut')
        }),
        ('Informations supplémentaires', {
            'fields': ('organisme', 'frais_inscription', 'documents_requis', 'lien_inscription'),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('actif', 'date_creation', 'date_modification'),
            'classes': ('collapse',)
        })
    )
