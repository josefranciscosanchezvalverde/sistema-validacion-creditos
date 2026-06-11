from django.contrib import admin
from .models import Credito
from django.utils.html import format_html  # 👈 IMPORTANTE

@admin.register(Credito)
class CreditoAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'numero_credito', 'semestre', 'estado', 'fecha_subida', 'ver_pdf')
    list_filter = ('estado', 'semestre')
    search_fields = ('alumno__username',)

    def ver_pdf(self, obj):
        if obj.archivo:
            return format_html(
                '<a href="{}" target="_blank">Ver PDF</a>',
                obj.archivo.url
            )
        return "Sin archivo"

    ver_pdf.short_description = "PDF"