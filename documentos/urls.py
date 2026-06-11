from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('portal/', views.portal_estudiante_view, name='portal_estudiante'),
    path('panel-admin/', views.panel_admin_view, name='panel_admin'),
    path('aprobar/<int:credito_id>/', views.aprobar_credito, name='aprobar_credito'),
    path('rechazar/<int:credito_id>/', views.rechazar_credito, name='rechazar_credito'),
    path('salir/', views.salir_view, name='salir'),
    path('gestion-admins/', views.gestion_administradores_view, name='gestion_administradores'),
    path('reset-password/', views.resetear_password_admin, name='resetear_password_admin'),
    # urls.py
    path('eliminar/<int:id>/', views.eliminar_estudiante, name='eliminar_estudiante'),
]