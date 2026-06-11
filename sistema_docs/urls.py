"""
URL configuration for sistema_docs project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # IMPORTANTE: Para leer settings.py
from django.conf.urls.static import static # IMPORTANTE: Para servir archivos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('documentos.urls')),
]

# 👇 ESTA ES LA PIEZA CLAVE 👇
# Le dice a Django: "Si alguien pide algo que empiece con /media/, 
# búscalo en la carpeta 'temp' (MEDIA_ROOT)"
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)