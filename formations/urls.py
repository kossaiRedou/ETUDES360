from django.urls import path
from . import views

app_name = 'formations'

urlpatterns = [
    path('', views.formations_list_view, name='list'),
    path('<int:pk>/', views.formation_detail_view, name='detail'),
]