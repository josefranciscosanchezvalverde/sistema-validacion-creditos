from pathlib import Path
import os

# 1. Ruta Base
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Seguridad y Desarrollo
SECRET_KEY = 'django-insecure-clave-residencias-teschi'
DEBUG = True
ALLOWED_HOSTS = ['*']

# 3. Aplicaciones
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'documentos',
]

# 4. Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # 🔥 EVITA CACHE (BACK BUTTON FIX)
    'documentos.middleware.NoCacheMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'sistema_docs.urls'

# 5. Plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Carpeta templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sistema_docs.wsgi.application'

# 6. Base de Datos (MySQL Workbench)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sistema_creditos', 
        'USER': 'root',             
        'PASSWORD': '1234', 
        'HOST': 'localhost',
        'PORT': '3307',
    }
}

# 7. Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]

# 8. Idioma y zona horaria
LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

# 9. Archivos estáticos
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

# 10. Tipo de llave primaria
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 👇 CONFIGURACIÓN DE RUTAS LOCALES (AQUÍ SE GUARDARÁN TUS PDF) 👇
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'temp')

# 11. =========================
# 📂 ALMACENAMIENTO LOCAL (CAMBIO AQUÍ)
# =========================
# Comentamos la línea de Google Drive para que Django use el disco duro local por defecto
# DEFAULT_FILE_STORAGE = 'gdstorage.storage.GoogleDriveStorage'

# Mantenemos estas por si las usas para otras funciones, pero ya no controlan el guardado de archivos
GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = os.path.join(BASE_DIR, 'credenciales.json')
GOOGLE_DRIVE_STORAGE_ROOT_ID = '1YotRqOcQPjveVIgiFxXkbrdDyBJxWHJk'

# 👇 RECOMENDACIÓN FINAL PARA EL VISOR (IFRAME) 👇
# ¡ESTA LÍNEA ES VITAL! Sin esto, el iframe saldrá en blanco por seguridad.
X_FRAME_OPTIONS = 'SAMEORIGIN'

CSRF_TRUSTED_ORIGINS = ['https://unshaken-maritime-fleshy.ngrok-free.dev']