from django.urls import path, include
from .views import proyectos_e_view


urlpatterns = [
    path('', proyectos_e_view, name="proyectos_e"),
]