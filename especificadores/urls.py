from django.urls import path

from . import views

app_name = "especificadores"

urlpatterns = [
    path("", views.especificadores_view, name="especificadores"),
    path("crear/", views.especificador_create_view, name="especificador_create"),
    path("<int:pk>/editar/", views.especificador_update_view, name="especificador_update"),
    path(
        "<int:pk>/toggle-activo/",
        views.especificador_toggle_activo_view,
        name="especificador_toggle_activo",
    ),
]
