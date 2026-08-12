from django.urls import path
from . import views, api_dashboard

app_name = "proyectos_c"


urlpatterns = [
    path('proyectos-c/', views.proyectos_c_view, name="proyectos_c"),
    path('proyectos-c/nuevo/', views.proyecto_c_create_view, name='proyecto_c_create'),
    path('proyectos-c/<int:pk>', views.proyectos_c_detail_view, name='proyecto_c_detail'),
    path('proyectos-c/<int:pk>/editar/', views.proyecto_c_update_view, name='proyecto_c_update'),
    path('proyectos-c-search/', views.proyectos_list_view, name='proyectos-c-list'),
    path('proyectos-c/<int:pk>/delete',views.proyecto_c_delete, name='proyecto_c_delete'),
    path('api/gantt-data/<int:pk>/', views.proyecto_gantt_data, name='proyecto_gantt_data'),

    # CSV exports consumidos por el pipeline local del dashboard de licitaciones.
    # Auth via header Authorization: Token <valor>  (env var DASHBOARD_EXPORT_TOKEN).
    path('api/dashboard/proyectos-cc.csv',
         api_dashboard.export_proyectos_cc_csv,
         name='api_export_proyectos_cc'),
    path('api/dashboard/proyectos-cc-licitacion.csv',
         api_dashboard.export_proyecto_cc_licitacion_csv,
         name='api_export_proyecto_cc_licitacion'),
    path('api/dashboard/proyectos-cc-estimador.csv',
         api_dashboard.export_proyecto_cc_estimador_csv,
         name='api_export_proyecto_cc_estimador'),
]

# urlpatterns = [
#     path('proyectos-e/', views.proyectos_e_view, name="proyectos_e"),
#     path('proyectos-e/<int:pk>', views.proyecto_E_detail_view, name='proyecto_e_detail'),
#     path('proyectos-e-search/', views.proyectos_list_view, name='proyectos-e-list'),
#     path('proyectos-e/<int:pk>/delete',views.proyecto_e_delete, name='proyecto_e_delete'),
# ]