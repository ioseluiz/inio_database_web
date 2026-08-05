from django.urls import path

from . import views

app_name = "estimadores"

urlpatterns = [
    path("", views.estimadores_view, name="estimadores"),
    path("crear/", views.estimador_create_view, name="estimador_create"),
    path("<int:pk>/editar/", views.estimador_update_view, name="estimador_update"),
    path(
        "<int:pk>/toggle-activo/",
        views.estimador_toggle_activo_view,
        name="estimador_toggle_activo",
    ),
]
