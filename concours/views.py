from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Concours
from core.models import Categorie

# Create your views here.

def concours_list_view(request):
    """Liste des concours avec filtres et recherche"""
    concours_queryset = Concours.objects.filter(actif=True).order_by('-date_creation')
    
    # Filtres
    search_term = request.GET.get('search', '')
    category = request.GET.get('category', 'all')
    level = request.GET.get('level', 'all')
    status = request.GET.get('status', 'all')
    
    if search_term:
        concours_queryset = concours_queryset.filter(
            Q(titre__icontains=search_term) |
            Q(description__icontains=search_term) |
            Q(organisme__icontains=search_term)
        )
    
    if category != 'all':
        concours_queryset = concours_queryset.filter(categorie__nom=category)
    
    if level != 'all':
        concours_queryset = concours_queryset.filter(niveau=level)
    
    if status != 'all':
        concours_queryset = concours_queryset.filter(statut=status)
    
    # Pagination
    paginator = Paginator(concours_queryset, 12)  # 12 concours par page
    page_number = request.GET.get('page')
    concours_page = paginator.get_page(page_number)
    
    # Données pour les filtres
    categories = Categorie.objects.all()
    
    context = {
        'concours_list': concours_page,
        'categories': categories,
        'search_term': search_term,
        'selected_category': category,
        'selected_level': level,
        'selected_status': status,
        'niveau_choices': Concours.NIVEAU_CHOICES,
        'status_choices': Concours.STATUS_CHOICES,
    }
    
    return render(request, 'concours/list.html', context)

def concours_detail_view(request, pk):
    """Détail d'un concours"""
    concours = get_object_or_404(Concours, pk=pk, actif=True)
    
    # Concours similaires
    similar_concours = Concours.objects.filter(
        categorie=concours.categorie,
        actif=True
    ).exclude(pk=concours.pk)[:3]
    
    context = {
        'concours': concours,
        'similar_concours': similar_concours,
    }
    
    return render(request, 'concours/detail.html', context)
