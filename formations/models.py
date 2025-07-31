from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import Categorie, Region

# Create your models here.

class Formation(models.Model):
    TYPE_CHOICES = [
        ('en_ligne', 'En ligne'),
        ('presentiel', 'Présentiel'),
        ('hybride', 'Hybride'),
    ]
    
    PRIX_CHOICES = [
        ('gratuite', 'Gratuite'),
        ('payante', 'Payante'),
    ]
    
    NIVEAU_CHOICES = [
        ('debutant', 'Débutant'),
        ('intermediaire', 'Intermédiaire'),
        ('avance', 'Avancé'),
        ('tous_niveaux', 'Tous niveaux'),
    ]
    
    titre = models.CharField(max_length=200)
    description = models.TextField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    type_formation = models.CharField(max_length=20, choices=TYPE_CHOICES)
    prix = models.CharField(max_length=20, choices=PRIX_CHOICES)
    prix_montant = models.CharField(max_length=100, blank=True)  # Ex: "500,000 GNF"
    duree = models.CharField(max_length=50)  # Ex: "6 mois", "3 semaines"
    niveau = models.CharField(max_length=20, choices=NIVEAU_CHOICES)
    date_debut = models.DateField()
    localisation = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    organisme = models.CharField(max_length=200)
    
    # Évaluation et statistiques
    note_moyenne = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    nombre_etudiants = models.PositiveIntegerField(default=0)
    certificat_disponible = models.BooleanField(default=False)
    
    # Informations supplémentaires
    prerequis = models.TextField(blank=True)
    programme = models.TextField(blank=True)
    objectifs = models.TextField(blank=True)
    lien_inscription = models.URLField(blank=True)
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True)
    
    def __str__(self):
        return self.titre
    
    @property
    def est_gratuite(self):
        return self.prix == 'gratuite'
    
    @property
    def note_etoiles(self):
        return int(self.note_moyenne)
    
    class Meta:
        verbose_name = "Formation"
        verbose_name_plural = "Formations"
        ordering = ['-date_creation']

class AvisFormation(models.Model):
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='avis')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    commentaire = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Avis de {self.utilisateur.username} sur {self.formation.titre}"
    
    class Meta:
        verbose_name = "Avis de formation"
        verbose_name_plural = "Avis de formations"
        unique_together = ['formation', 'utilisateur']
        ordering = ['-date_creation']
