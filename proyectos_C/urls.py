from django.urls import path
from . import views

app_name = "proyectos_c"


urlpatterns = [
    path('proyectos-c/', views.proyectos_c_view, name="proyectos_c"),
    path('proyectos-c/<int:pk>', views.proyectos_c_detail_view, name='proyecto_c_detail')
]