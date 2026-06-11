from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
from django.conf import settings
import os

# ✅ ID DEFINITIVO DE LA CARPETA EN LA UNIDAD COMPARTIDA
FOLDER_ID = "1gADTM8S85frklhAJqNXyz7BM2JuQfA0K"

def obtener_o_crear_carpeta_alumno(service, matricula):
    """
    Busca si ya existe una carpeta con la matrícula en Drive. 
    Si existe, devuelve su ID. Si no, la crea y devuelve el nuevo ID.
    """
    try:
        query = f"name = '{matricula}' and '{FOLDER_ID}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        
        resultados = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)',
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()
        
        archivos = resultados.get('files', [])
        
        if archivos:
            print(f"📁 La carpeta del alumno con matrícula {matricula} ya existe.")
            return archivos[0]['id']
        else:
            print(f"✨ Creando carpeta automática para la matrícula: {matricula}...")
            meta_carpeta = {
                'name': matricula,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [FOLDER_ID]
            }
            nueva_carpeta = service.files().create(
                body=meta_carpeta,
                fields='id',
                supportsAllDrives=True
            ).execute()
            return nueva_carpeta.get('id')
            
    except Exception as e:
        print(f"❌ Error al buscar/crear carpeta de la matrícula: {str(e)}")
        return None

def subir_a_drive(ruta_archivo, nombre_archivo, matricula):
    """
    Sube el archivo PDF dentro de la carpeta específica de la matrícula del alumno.
    """
    try:
        print("1. Buscando archivo de credenciales...")
        SCOPES = ['https://www.googleapis.com/auth/drive']
        
        if not os.path.exists(settings.GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE):
            print(f"❌ Error: No se encontró el archivo JSON en: {settings.GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE}")
            return None

        creds = service_account.Credentials.from_service_account_file(
            settings.GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE,
            scopes=SCOPES
        )

        print("2. Conectando con el servicio de Google Drive...")
        service = build('drive', 'v3', credentials=creds)

        print(f"3. Verificando archivo local: {ruta_archivo}")
        if not os.path.exists(ruta_archivo):
            print(f"❌ Error: El archivo PDF físico no existe en la ruta: {ruta_archivo}")
            return None

        # Obtenemos el ID de la subcarpeta del alumno
        id_carpeta_destino = obtener_o_crear_carpeta_alumno(service, matricula)
        if not id_carpeta_destino:
            id_carpeta_destino = FOLDER_ID

        file_metadata = {
            'name': nombre_archivo,
            'parents': [id_carpeta_destino]
        }

        print(f"4. Preparando subida dentro de la carpeta {matricula}...")
        media = MediaFileUpload(ruta_archivo, mimetype='application/pdf', resumable=False)

        print("5. Enviando archivo a Google Drive (create)...")
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink',
            supportsAllDrives=True
        ).execute()

        print(f"✅ Archivo subido exitosamente a la carpeta del alumno {matricula}. ID Archivo:", file.get('id'))
        return file.get('webViewLink')

    except Exception as e:
        print("❌ Error crítico en subir_a_drive:", str(e))
        import traceback
        traceback.print_exc()
        return None