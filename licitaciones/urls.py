from django.urls import path
from . import views

app_name = "licitaciones"

urlpatterns = [
    path('licitaciones/', views.licitaciones_view, name="licitaciones"),
    path('licitaciones/<int:pk>', views.licitaciones_detail_view, name='licitaciones_detail'),
    path('licitaciones-search/', views.licitaciones_list_view, name='licitaciones-list'),
    
]