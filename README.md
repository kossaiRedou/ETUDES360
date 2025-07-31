# 🎓 Etudes360 - Plateforme Éducative Guinéenne

Plateforme web dédiée aux opportunités éducatives en Guinée : formations, concours et bourses d'études.

## 🚀 Fonctionnalités

- **📚 Formations** : Catalogue de formations professionnelles et techniques
- **🏆 Concours** : Concours d'entrée dans les écoles et universités
- **💰 Bourses** : Bourses d'études nationales et internationales
- **👤 Profils utilisateurs** : Gestion des candidatures et favoris
- **🔍 Recherche avancée** : Filtrage par catégorie, région, niveau

## 🛠️ Technologies

- **Backend** : Django 5.2.4, Python 3.12
- **Frontend** : HTML5, Tailwind CSS, JavaScript
- **Base de données** : SQLite (développement)
- **Authentification** : Django Auth
- **Déploiement** : Ngrok (développement)

## 📦 Installation

### Prérequis
- Python 3.12+
- Environnement virtuel `env360`

### Étapes d'installation

1. **Cloner le projet :**
   ```bash
   git clone <url-du-repo>
   cd GABITHEX
   ```

2. **Activer l'environnement virtuel :**
   ```bash
   # Windows
   ..\env360\Scripts\activate

   # Linux/Mac
   source ../env360/bin/activate
   ```

3. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer les variables d'environnement :**
   ```bash
   cp .env.example .env
   # Éditer .env avec vos valeurs
   ```

5. **Migrer la base de données :**
   ```bash
   python manage.py migrate
   ```

6. **Charger les données d'exemple :**
   ```bash
   python insert_data.py      # Formations
   python insert_concours.py  # Concours
   python insert_bourses.py   # Bourses
   ```

7. **Créer un superutilisateur :**
   ```bash
   python manage.py createsuperuser
   ```

8. **Lancer le serveur :**
   ```bash
   python manage.py runserver
   ```

## 🌐 Partage avec ngrok

Pour partager votre travail :

1. **Installer ngrok** : [ngrok.com](https://ngrok.com)
2. **Lancer Django** : `python manage.py runserver 0.0.0.0:8000`
3. **Lancer ngrok** : `ngrok http 8000`
4. **Partager l'URL** générée par ngrok

## 📁 Structure du projet

```
GABITHEX/
├── core/              # App principale (authentification, profils)
├── formations/        # Gestion des formations
├── concours/          # Gestion des concours
├── bourses/           # Gestion des bourses
├── static/            # Fichiers statiques (CSS, JS, images)
├── templates/         # Templates HTML
├── GABITHEX/          # Configuration Django
├── manage.py          # Point d'entrée Django
├── .env.example       # Template de configuration
└── README.md          # Ce fichier
```

## 🎨 Design

- **Logo** : Etudes360 avec couleurs personnalisées
- **Couleurs principales** :
  - Bleu foncé : `#0f2342`
  - Vert : `#7bc1a2`
  - Blanc cassé : `#f2f2eb`
- **Framework CSS** : Tailwind CSS
- **Icons** : Lucide React (CDN)

## 📊 Données

Le projet inclut des données réelles :
- **5 formations** (CMI Guinée, INFP, Marketing Digital...)
- **3 concours** (CFP, ENPT, ISMGB...)
- **3 bourses** (DAAD, MasterCard Foundation, Eiffel...)

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit les changes (`git commit -m 'Ajout nouvelle fonctionnalité'`)
4. Push sur la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👥 Auteurs

- **Développeur principal** : GABITHEX
- **Design** : Inspiré du logo Etudes360

## 🆘 Support

Pour toute question ou problème :
- Ouvrir une issue sur GitHub
- Contacter : aliou@gabithex.fr

---

**Etudes360** - *Votre portail vers l'excellence éducative en Guinée* 🇬🇳