from django.urls import path
from . import views

app_name = 'bourses'

urlpatterns = [
    path('', views.bourses_list_view, name='list'),
    path('<int:pk>/', views.bourse_detail_view, name='detail'),
]