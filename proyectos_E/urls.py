from django.urls import path, include
from .views import proyectos_e_view, proyecto_E_detail_view


urlpatterns = [
    path('proyectos-e/', proyectos_e_view, name="proyectos_e"),
    path('proyectos-e/<int:pk>', proyecto_E_detail_view, name='proyecto_e_detail')
]