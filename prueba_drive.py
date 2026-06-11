import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Si cambiaste los permisos en la consola de Google, asegúrate de que coincidan aquí
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def obtener_servicio():
    creds = None
    # El archivo token.pickle almacena los permisos del usuario
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
    # Si no hay credenciales válidas, deja que el usuario inicie sesión
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Guarda las credenciales para la próxima vez
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

try:
    service = obtener_servicio()
    print("¡Conexión exitosa! Ya puedes ver tus archivos o subir documentos.")
except Exception as e:
    print(f"Hubo un error: {e}")