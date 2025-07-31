from django.contrib import admin
from .models import Region, Categorie, UserProfile

# Register your models here.

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['nom', 'code']
    search_fields = ['nom', 'code']

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'description', 'couleur']
    search_fields = ['nom']
    list_filter = ['couleur']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'telephone', 'region', 'niveau_etudes']
    search_fields = ['user__username', 'user__email', 'telephone']
    list_filter = ['region', 'niveau_etudes']
    filter_horizontal = ['domaines_interet']
