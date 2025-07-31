from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Formation
from core.models import Categorie

# Create your views here.

def formations_list_view(request):
    """Liste des formations avec filtres"""
    formations_queryset = Formation.objects.filter(actif=True).order_by('-date_creation')
    
    # Filtres basiques
    search_term = request.GET.get('search', '')
    if search_term:
        formations_queryset = formations_queryset.filter(
            Q(titre__icontains=search_term) |
            Q(description__icontains=search_term)
        )
    
    # Pagination
    paginator = Paginator(formations_queryset, 12)
    page_number = request.GET.get('page')
    formations_page = paginator.get_page(page_number)
    
    context = {
        'formations_list': formations_page,
        'search_term': search_term,
    }
    
    return render(request, 'formations/list.html', context)

def formation_detail_view(request, pk):
    """Détail d'une formation"""
    formation = get_object_or_404(Formation, pk=pk, actif=True)
    
    context = {
        'formation': formation,
    }
    
    return render(request, 'formations/detail.html', context)
