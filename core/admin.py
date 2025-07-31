from django.contrib import admin
from .models import Region, Categorie, UserProfile, Contact

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


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Administration des messages de contact"""
    list_display = ['nom', 'email', 'sujet', 'statut', 'date_creation', 'date_reponse']
    list_filter = ['sujet', 'statut', 'date_creation']
    search_fields = ['nom', 'email', 'message']
    readonly_fields = ['date_creation', 'date_modification']
    list_editable = ['statut']
    
    fieldsets = (
        ('Informations du contact', {
            'fields': ('nom', 'email', 'telephone', 'sujet')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Gestion', {
            'fields': ('statut', 'reponse', 'date_reponse')
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Mettre à jour la date de réponse automatiquement"""
        if 'reponse' in form.changed_data and obj.reponse and not obj.date_reponse:
            from django.utils import timezone
            obj.date_reponse = timezone.now()
        super().save_model(request, obj, form, change)
