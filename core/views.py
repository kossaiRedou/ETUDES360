from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Count
from concours.models import Concours
from formations.models import Formation
from bourses.models import Bourse
from .models import UserProfile, Region, Categorie, Contact
from .forms import CustomUserCreationForm, UserProfileForm, CustomAuthenticationForm, ContactForm

# Create your views here.

def home_view(request):
    """Page d'accueil avec les opportunités récentes"""
    # Récupérer les opportunités récentes (exactement comme dans Next.js)
    recent_concours = Concours.objects.filter(actif=True).order_by('-date_creation')[:2]
    recent_formations = Formation.objects.filter(actif=True).order_by('-date_creation')[:2]
    recent_bourses = Bourse.objects.filter(actif=True).order_by('-date_creation')[:2]
    
    # Combiner toutes les opportunités récentes
    recent_opportunities = []
    
    for concours in recent_concours:
        recent_opportunities.append({
            'id': concours.id,
            'title': concours.titre,
            'type': 'Concours',
            'deadline': concours.deadline.strftime('%d %B %Y'),
            'category': concours.categorie.nom,
            'description': concours.description[:100] + '...' if len(concours.description) > 100 else concours.description,
            'url': f'/concours/{concours.id}/',
        })
    
    for formation in recent_formations:
        recent_opportunities.append({
            'id': formation.id,
            'title': formation.titre,
            'type': 'Formation',
            'deadline': formation.date_debut.strftime('%d %B %Y'),
            'category': formation.categorie.nom,
            'description': formation.description[:100] + '...' if len(formation.description) > 100 else formation.description,
            'url': f'/formations/{formation.id}/',
        })
    
    for bourse in recent_bourses:
        recent_opportunities.append({
            'id': bourse.id,
            'title': bourse.titre,
            'type': 'Bourse',
            'deadline': bourse.deadline.strftime('%d %B %Y'),
            'category': bourse.pays_destination.nom,
            'description': bourse.description[:100] + '...' if len(bourse.description) > 100 else bourse.description,
            'url': f'/bourses/{bourse.id}/',
        })
    
    # Statistiques
    stats = {
        'total_concours': Concours.objects.filter(actif=True).count(),
        'total_formations': Formation.objects.filter(actif=True).count(),
        'total_bourses': Bourse.objects.filter(actif=True).count(),
        'total_users': UserProfile.objects.count(),
    }
    
    context = {
        'recent_opportunities': recent_opportunities[:6],  # Limiter à 6 comme dans Next.js
        'stats': stats,
    }
    
    return render(request, 'core/home.html', context)

def login_view(request):
    """Vue de connexion"""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Essayer de se connecter avec le nom d'utilisateur
            user = authenticate(request, username=username, password=password)
            
            # Si ça ne marche pas, essayer avec l'email
            if user is None:
                try:
                    from django.contrib.auth.models import User
                    user_obj = User.objects.get(email=username)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Connexion réussie!')
                return redirect('core:home')
            else:
                messages.error(request, 'Email/nom d\'utilisateur ou mot de passe incorrect.')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'core/auth.html', {'mode': 'login', 'form': form})

def register_view(request):
    """Vue d'inscription"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Créer le profil utilisateur
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Compte créé avec succès! Bienvenue sur Etudes360!')
            return redirect('core:home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'core/auth.html', {'mode': 'register', 'form': form})

@login_required
def profile_view(request):
    """Vue du profil utilisateur"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    regions = Region.objects.all()
    categories = Categorie.objects.all()
    
    if request.method == 'POST':
        # Mettre à jour le profil
        profile.telephone = request.POST.get('telephone', '')
        profile.bio = request.POST.get('bio', '')
        
        region_id = request.POST.get('region')
        if region_id:
            profile.region_id = region_id
        
        profile.niveau_etudes = request.POST.get('niveau_etudes', '')
        profile.save()
        
        # Mettre à jour les domaines d'intérêt
        domaines_ids = request.POST.getlist('domaines_interet')
        profile.domaines_interet.set(domaines_ids)
        
        messages.success(request, 'Profil mis à jour avec succès!')
        return redirect('core:profile')
    
    context = {
        'profile': profile,
        'regions': regions,
        'categories': categories,
    }
    
    return render(request, 'core/profile.html', context)

def logout_view(request):
    """Vue de déconnexion"""
    logout(request)
    messages.success(request, 'Déconnexion réussie!')
    return redirect('core:home')

def contact_view(request):
    """Vue de contact utilisant Django au maximum"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Django sauvegarde automatiquement avec ModelForm
            contact = form.save()
            messages.success(
                request, 
                f'Merci {contact.nom} ! Votre message a été envoyé avec succès. '
                f'Nous vous répondrons dans les plus brefs délais à {contact.email}.'
            )
            return redirect('core:contact')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = ContactForm()
        # Pré-remplir avec les infos de l'utilisateur connecté
        if request.user.is_authenticated:
            form.initial = {
                'nom': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                'email': request.user.email,
            }
    
    # Statistiques pour la page contact
    stats = {
        'messages_total': Contact.objects.count(),
        'messages_resolus': Contact.objects.filter(statut='resolu').count(),
        'temps_reponse_moyen': '24h',  # Vous pouvez calculer cela dynamiquement
    }
    
    context = {
        'form': form,
        'stats': stats,
    }
    
    return render(request, 'core/contact.html', context)
