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


class Contact(models.Model):
    """Modèle pour les messages de contact"""
    SUJET_CHOICES = [
        ('question', 'Question générale'),
        ('formation', 'Question sur une formation'),
        ('concours', 'Question sur un concours'),
        ('bourse', 'Question sur une bourse'),
        ('technique', 'Problème technique'),
        ('autre', 'Autre'),
    ]
    
    STATUS_CHOICES = [
        ('nouveau', 'Nouveau'),
        ('en_cours', 'En cours de traitement'),
        ('resolu', 'Résolu'),
        ('ferme', 'Fermé'),
    ]
    
    nom = models.CharField(max_length=100, verbose_name="Nom complet")
    email = models.EmailField(verbose_name="Email")
    telephone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    sujet = models.CharField(max_length=20, choices=SUJET_CHOICES, verbose_name="Sujet")
    message = models.TextField(verbose_name="Message")
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='nouveau', verbose_name="Statut")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    reponse = models.TextField(blank=True, verbose_name="Réponse de l'équipe")
    date_reponse = models.DateTimeField(null=True, blank=True, verbose_name="Date de réponse")
    
    def __str__(self):
        return f"{self.nom} - {self.get_sujet_display()}"
    
    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-date_creation']
