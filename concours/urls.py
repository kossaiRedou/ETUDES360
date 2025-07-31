from django.urls import path
from . import views

app_name = 'concours'

urlpatterns = [
    path('', views.concours_list_view, name='list'),
    path('<int:pk>/', views.concours_detail_view, name='detail'),
]