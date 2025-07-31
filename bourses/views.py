from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Bourse, Pays

# Create your views here.

def bourses_list_view(request):
    """Liste des bourses avec filtres"""
    bourses_queryset = Bourse.objects.filter(actif=True).order_by('-date_creation')
    
    # Filtres basiques
    search_term = request.GET.get('search', '')
    if search_term:
        bourses_queryset = bourses_queryset.filter(
            Q(titre__icontains=search_term) |
            Q(description__icontains=search_term)
        )
    
    # Pagination
    paginator = Paginator(bourses_queryset, 12)
    page_number = request.GET.get('page')
    bourses_page = paginator.get_page(page_number)
    
    context = {
        'bourses_list': bourses_page,
        'search_term': search_term,
    }
    
    return render(request, 'bourses/list.html', context)

def bourse_detail_view(request, pk):
    """Détail d'une bourse"""
    bourse = get_object_or_404(Bourse, pk=pk, actif=True)
    
    context = {
        'bourse': bourse,
    }
    
    return render(request, 'bourses/detail.html', context)
