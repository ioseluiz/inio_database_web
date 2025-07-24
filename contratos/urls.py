from django.urls import path
from . import views

app_name = "contratos"

urlpatterns = [
    path('contratos/', views.contratos_view, name="contratos"),
    path('contratos/<int:pk>', views.contratos_detail_view, name='contratos_detail'),
    path('contratos-search/', views.contratos_list_view, name='contratos-list'),
    path('contratos/<int:pk>/delete',views.contratos_delete_view, name='contratos_delete'),
]