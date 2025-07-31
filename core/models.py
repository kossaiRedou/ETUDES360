from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Region(models.Model):
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "Région"
        verbose_name_plural = "Régions"

class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    couleur = models.CharField(max_length=7, default="#000000")  # Code couleur hex
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

class UserProfile(models.Model):
    NIVEAUX_ETUDES = [
        ('college', 'Collège'),
        ('lycee', 'Lycée'),
        ('licence', 'Université (L1-L3)'),
        ('master', 'Master'),
        ('doctorat', 'Doctorat'),
        ('professionnel', 'Formation professionnelle'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    niveau_etudes = models.CharField(max_length=20, choices=NIVEAUX_ETUDES, blank=True)
    domaines_interet = models.ManyToManyField(Categorie, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return f"Profil de {self.user.username}"
    
    class Meta:
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils utilisateurs"
