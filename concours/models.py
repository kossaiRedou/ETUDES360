from django.db import models
from django.utils import timezone
from core.models import Categorie, Region

# Create your models here.

class Concours(models.Model):
    STATUS_CHOICES = [
        ('ouvert', 'Ouvert'),
        ('ferme', 'Fermé'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
    ]
    
    NIVEAU_CHOICES = [
        ('college', 'Collège'),
        ('lycee', 'Lycée'),
        ('superieur', 'Supérieur'),
        ('professionnel', 'Professionnel'),
    ]
    
    titre = models.CharField(max_length=200)
    description = models.TextField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    niveau = models.CharField(max_length=20, choices=NIVEAU_CHOICES)
    deadline = models.DateTimeField()
    localisation = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    nombre_places = models.CharField(max_length=50)  # Ex: "200 places" ou "500 postes"
    prerequis = models.TextField()
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ouvert')
    
    # Informations supplémentaires
    organisme = models.CharField(max_length=200, blank=True)
    frais_inscription = models.CharField(max_length=100, blank=True)
    documents_requis = models.TextField(blank=True)
    lien_inscription = models.URLField(blank=True)
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True)
    
    def __str__(self):
        return self.titre
    
    @property
    def est_ouvert(self):
        return self.statut == 'ouvert' and self.deadline > timezone.now()
    
    @property
    def jours_restants(self):
        if self.deadline > timezone.now():
            delta = self.deadline - timezone.now()
            return delta.days
        return 0
    
    class Meta:
        verbose_name = "Concours"
        verbose_name_plural = "Concours"
        ordering = ['-date_creation']
