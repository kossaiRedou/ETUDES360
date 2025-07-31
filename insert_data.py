#!/usr/bin/env python
"""
Script pour injecter les données de formations dans la base de données
Usage: python insert_data.py
"""

import os
import sys
import django

# Configuration Django - DOIT être fait AVANT tout import de modèles
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GABITHEX.settings')
django.setup()

# Maintenant on peut importer les modèles Django
from formations.models import Formation
from core.models import Categorie

def main():
    print("=" * 50)
    print("🚀 INJECTION DES DONNÉES ETUDES360")
    print("=" * 50)
    
    # Créer les catégories de base
    print("\n📂 Création des catégories...")
    categories_data = [
        {'nom': 'Technique et Industriel', 'description': 'Formations techniques et industrielles', 'couleur': '#3B82F6'},
        {'nom': 'Gestion et Administration', 'description': 'Formations en gestion et administration', 'couleur': '#10B981'},
        {'nom': 'Commerce et Marketing', 'description': 'Formations commerciales et marketing', 'couleur': '#F59E0B'},
        {'nom': 'Agriculture et Environnement', 'description': 'Formations agricoles et environnementales', 'couleur': '#22C55E'},
    ]

    categories_created = 0
    for cat_data in categories_data:
        category, created = Categorie.objects.get_or_create(
            nom=cat_data['nom'],
            defaults=cat_data
        )
        if created:
            categories_created += 1
            print(f'✅ Catégorie créée: {category.nom}')
        else:
            print(f'ℹ️  Catégorie existe: {category.nom}')

    # Données des formations
    print("\n🎓 Chargement des formations...")
    formations_data = [
        {
            "titre": "Conduite d'engins lourds – CMI Guinée",
            "description": "Formation pratique et théorique à la conduite de chargeuses, bulldozers, chariots élévateurs, véhicules lourds.",
            "categorie_nom": "Technique et Industriel",
            "type_formation": "presentiel",
            "prix": "payante",
            "prix_montant": "Non spécifié",
            "duree": "6 mois",
            "niveau": "debutant",
            "date_debut": "2025-09-01",
            "localisation": "Conakry (et centres Kankan, Nzérékoré, Boké…)",
            "organisme": "Centre des Métiers Industriels (CMI‑Guinée)",
            "certificat_disponible": True,
            "prerequis": "Aucun requis spécifique",
            "programme": "Conduite et maintenance engins lourds, sécurité, logistique",
            "objectifs": "Former des conducteurs professionnels certifiés",
            "lien_inscription": "https://cmi-guinee.com",
            "actif": True
        },
        {
            "titre": "Certificat Santé & Sécurité au Travail – INFP",
            "description": "Programme en santé et sécurité pour cadres et personnel administratif.",
            "categorie_nom": "Gestion et Administration",
            "type_formation": "presentiel",
            "prix": "payante",
            "prix_montant": "Non spécifié",
            "duree": "5 jours",
            "niveau": "intermediaire",
            "date_debut": "2025-08-15",
            "localisation": "Conakry",
            "organisme": "INFP Guinée",
            "certificat_disponible": True,
            "prerequis": "Être cadre ou agent public",
            "programme": "Réglementation HSE, prévention, outils pratiques",
            "objectifs": "Renforcer les capacités en HSS en milieu professionnel",
            "lien_inscription": "https://infpguinee.com",
            "actif": True
        },
        {
            "titre": "Formation Marketing Digital – International Skills Academy",
            "description": "Cours à distance sur publicité Facebook et Google Ads, management de projet, etc.",
            "categorie_nom": "Commerce et Marketing",
            "type_formation": "en_ligne",
            "prix": "payante",
            "prix_montant": "1 000 000 GNF (1 mois)",
            "duree": "1 mois",
            "niveau": "intermediaire",
            "date_debut": "2025-09-01",
            "localisation": "En ligne",
            "organisme": "International Skills Academy (Guinée)",
            "certificat_disponible": True,
            "prerequis": "Accès Internet, niveau bac souhaité",
            "programme": "Facebook Ads, Google Ads, management de projet",
            "objectifs": "Développer des compétences marketing digital",
            "lien_inscription": "https://www.isaworld.net/gn",
            "actif": True
        },
        {
            "titre": "Agro-transformation & Aviculture – ASCAD Guinée",
            "description": "Formation professionnelle en agroalimentaire et aviculture, conduite poids lourds, plomberie, etc.",
            "categorie_nom": "Agriculture et Environnement",
            "type_formation": "presentiel",
            "prix": "payante",
            "prix_montant": "Non spécifié",
            "duree": "4 semaines",
            "niveau": "debutant",
            "date_debut": "2025-09-15",
            "localisation": "Conakry, Kindia, Kankan, Mamou, Boké",
            "organisme": "ASCAD Guinée (SCAD)",
            "certificat_disponible": True,
            "prerequis": "18–40 ans, volontariat",
            "programme": "Agriculture, élevage, aviculture, conduite poids lourds, plomberie, métallurgie",
            "objectifs": "Insertion socio‑professionnelle des jeunes",
            "lien_inscription": "https://www.ascadguinee.org",
            "actif": True
        },
        {
            "titre": "Certificat en Logistique & Transport – Guinée WorkForce",
            "description": "Formation financée par l'ONFPP en logistique et transport conduite défensive.",
            "categorie_nom": "Technique et Industriel",
            "type_formation": "presentiel",
            "prix": "payante",
            "prix_montant": "Non spécifié",
            "duree": "10 jours",
            "niveau": "intermediaire",
            "date_debut": "2025-08-01",
            "localisation": "Conakry",
            "organisme": "Guinée WorkForce (avec ONFPP)",
            "certificat_disponible": True,
            "prerequis": "Être conducteur ou personnel opérationnel",
            "programme": "Logistique, transport, conduite défensive, sécurité",
            "objectifs": "Améliorer performance en transport et sécurité",
            "lien_inscription": "https://guinee-workforce.com",
            "actif": True
        }
    ]

    formations_created = 0
    formations_updated = 0

    for formation_data in formations_data:
        # Récupérer la catégorie
        try:
            categorie = Categorie.objects.get(nom=formation_data['categorie_nom'])
        except Categorie.DoesNotExist:
            print(f'❌ Catégorie "{formation_data["categorie_nom"]}" non trouvée')
            continue

        # Créer ou mettre à jour la formation
        formation, created = Formation.objects.update_or_create(
            titre=formation_data['titre'],
            defaults={
                'description': formation_data['description'],
                'categorie': categorie,
                'type_formation': formation_data['type_formation'],
                'prix': formation_data['prix'],
                'prix_montant': formation_data['prix_montant'],
                'duree': formation_data['duree'],
                'niveau': formation_data['niveau'],
                'date_debut': formation_data['date_debut'],
                'localisation': formation_data['localisation'],
                'organisme': formation_data['organisme'],
                'note_moyenne': 0.0,
                'nombre_etudiants': 0,
                'certificat_disponible': formation_data['certificat_disponible'],
                'prerequis': formation_data['prerequis'],
                'programme': formation_data['programme'],
                'objectifs': formation_data['objectifs'],
                'lien_inscription': formation_data['lien_inscription'],
                'actif': formation_data['actif']
            }
        )
        
        if created:
            formations_created += 1
            print(f'✅ Formation créée: {formation.titre}')
        else:
            formations_updated += 1
            print(f'🔄 Formation mise à jour: {formation.titre}')

    # Rapport final
    print("\n" + "=" * 50)
    print("🎉 INJECTION TERMINÉE AVEC SUCCÈS!")
    print("=" * 50)
    print(f"📊 Résumé:")
    print(f"   • Catégories créées: {categories_created}")
    print(f"   • Formations créées: {formations_created}")
    print(f"   • Formations mises à jour: {formations_updated}")
    print(f"\n📈 Totaux en base:")
    print(f"   • Total catégories: {Categorie.objects.count()}")
    print(f"   • Total formations: {Formation.objects.count()}")
    print("\n🚀 Lancez maintenant: python manage.py runserver")
    print("=" * 50)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERREUR: {str(e)}")
        print("💡 Assurez-vous que:")
        print("   1. L'environnement virtuel env360 est activé")
        print("   2. Vous êtes dans le répertoire GABITHEX")
        print("   3. La base de données est migrée (python manage.py migrate)")
        sys.exit(1)