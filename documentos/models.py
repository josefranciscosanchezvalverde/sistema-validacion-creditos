from django.db import models
from django.contrib.auth.models import User
import os
from .utils_drive import subir_a_drive

def ruta_carpeta_alumno(instance, filename):
    matricula = instance.alumno.username
    return f'{matricula}/{filename}'

class Credito(models.Model):
    alumno = models.ForeignKey(User, on_delete=models.CASCADE)
    numero_credito = models.IntegerField(default=1)
    semestre = models.IntegerField()
    
    archivo = models.FileField(
        upload_to=ruta_carpeta_alumno, 
        null=True, 
        blank=True
    )

    link_drive = models.URLField(blank=True, null=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='En Revisión')
    comentarios_admin = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.alumno.first_name} - Crédito {self.numero_credito}"

    def save(self, *args, **kwargs):
        # Si el estado es "Aprobado" y aún no tiene link de Drive, lo subimos
        if self.estado and self.estado.lower() == "aprobado" and not self.link_drive:
            if self.archivo:
                ruta_local = self.archivo.path
                nombre_archivo = os.path.basename(self.archivo.name)
                
                # Extraemos la matrícula del estudiante
                matricula_alumno = str(self.alumno.username)

                print(f"⚠️ Detectado estado 'Aprobado'. Iniciando subida a Drive para alumno {matricula_alumno}...")
                
                # Ejecutamos la subida
                link_resultado = subir_a_drive(ruta_local, nombre_archivo, matricula_alumno)
                
                # Guardamos el link en la base de datos
                if link_resultado:
                    self.link_drive = link_resultado

        super().save(*args, **kwargs)