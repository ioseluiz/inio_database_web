from django.urls import path
from . import views

app_name = "proyectos_e"


urlpatterns = [
    path('proyectos-e/', views.proyectos_e_view, name="proyectos_e"),
    path('proyectos-e/<int:pk>', views.proyecto_E_detail_view, name='proyecto_e_detail'),
    path('proyectos-e-search/', views.proyectos_list_view, name='proyectos-e-list'),
    path('proyectos-e/<int:pk>/delete',views.proyecto_e_delete, name='proyecto_e_delete'),
]