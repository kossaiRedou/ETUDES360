from django.db import models
from django.utils import timezone
from core.models import Categorie, Region

# Create your models here.

class Pays(models.Model):
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=3, unique=True)  # Ex: "FR", "CA", "CN"
    continent = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "Pays"
        verbose_name_plural = "Pays"

class Bourse(models.Model):
    TYPE_CHOICES = [
        ('complete', 'Complète'),
        ('partielle', 'Partielle'),
        ('logement', 'Logement'),
        ('transport', 'Transport'),
    ]
    
    NIVEAU_CHOICES = [
        ('licence', 'Licence'),
        ('master', 'Master'),
        ('doctorat', 'Doctorat'),
        ('master_doctorat', 'Master/Doctorat'),
        ('licence_master_doctorat', 'Licence/Master/Doctorat'),
        ('postdoc', 'Post-doctorat'),
    ]
    
    titre = models.CharField(max_length=200)
    description = models.TextField()
    pays_destination = models.ForeignKey(Pays, on_delete=models.CASCADE)
    niveau = models.CharField(max_length=30, choices=NIVEAU_CHOICES)
    type_bourse = models.CharField(max_length=20, choices=TYPE_CHOICES)
    montant = models.CharField(max_length=100)  # Ex: "100% des frais + allocation", "1,181€/mois"
    deadline = models.DateTimeField()
    duree = models.CharField(max_length=50)  # Ex: "2-4 ans", "1 an renouvelable"
    
    # Informations détaillées
    domaines_etudes = models.ManyToManyField(Categorie, blank=True)
    domaines_texte = models.TextField(blank=True)  # Pour domaines spécifiques
    prerequis = models.TextField()
    organisme = models.CharField(max_length=200)
    nombre_places = models.PositiveIntegerField()
    
    # Critères d'éligibilité
    age_minimum = models.PositiveIntegerField(null=True, blank=True)
    age_maximum = models.PositiveIntegerField(null=True, blank=True)
    moyenne_requise = models.CharField(max_length=50, blank=True)  # Ex: "Mention Bien minimum"
    test_langue_requis = models.CharField(max_length=100, blank=True)  # Ex: "IELTS 6.5", "DELF B2"
    
    # Informations supplémentaires
    avantages_supplementaires = models.TextField(blank=True)
    documents_requis = models.TextField(blank=True)
    lien_candidature = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True)
    
    def __str__(self):
        return self.titre
    
    @property
    def est_ouverte(self):
        return self.deadline > timezone.now() and self.actif
    
    @property
    def jours_restants(self):
        if self.deadline > timezone.now():
            delta = self.deadline - timezone.now()
            return delta.days
        return 0
    
    @property
    def est_complete(self):
        return self.type_bourse == 'complete'
    
    class Meta:
        verbose_name = "Bourse"
        verbose_name_plural = "Bourses"
        ordering = ['-date_creation']

class CandidatureBourse(models.Model):
    STATUS_CHOICES = [
        ('en_preparation', 'En préparation'),
        ('soumise', 'Soumise'),
        ('en_attente', 'En attente'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
    ]
    
    bourse = models.ForeignKey(Bourse, on_delete=models.CASCADE, related_name='candidatures')
    utilisateur = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_preparation')
    date_candidature = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    notes_personnelles = models.TextField(blank=True)
    
    def __str__(self):
        return f"Candidature de {self.utilisateur.username} pour {self.bourse.titre}"
    
    class Meta:
        verbose_name = "Candidature de bourse"
        verbose_name_plural = "Candidatures de bourses"
        unique_together = ['bourse', 'utilisateur']
        ordering = ['-date_candidature']
