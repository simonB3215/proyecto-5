import os
import uuid
import magic
import requests
from db.supabase_client import get_base_url, get_headers

# Extensiones permitidas (MVP)
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.pdf', '.webp'}

# Tipos MIME permitidos
ALLOWED_MIMES = {
    'image/jpeg',
    'image/png',
    'application/pdf',
    'image/webp'
}

# Límite de tamaño: 5MB
MAX_FILE_SIZE = 5 * 1024 * 1024

BUCKET_NAME = "documentos_garantia"

def validate_and_save_file(uploaded_file_path):
    """
    Valida un archivo subido y lo sube al Storage de Supabase usando REST.
    Retorna la URL pública del archivo y su tipo MIME.
    """
    # 1. Verificar tamaño
    file_size = os.path.getsize(uploaded_file_path)
    if file_size > MAX_FILE_SIZE:
        raise ValueError("El archivo excede el tamaño máximo permitido (5MB).")

    # 2. Verificar extensión
    _, ext = os.path.splitext(uploaded_file_path)
    ext = ext.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Extensión no permitida: {ext}")

    # 3. Verificar MIME type real
    mime = magic.Magic(mime=True)
    file_mime = mime.from_file(uploaded_file_path)
    if file_mime not in ALLOWED_MIMES:
        raise ValueError(f"Tipo MIME no permitido: {file_mime}")

    # 4. Generar nombre seguro
    safe_filename = f"{uuid.uuid4()}{ext}"

    # 5. Subir a Supabase Storage (REST)
    url = get_base_url()
    headers = get_headers().copy()
    headers["Content-Type"] = file_mime
    
    try:
        with open(uploaded_file_path, 'rb') as f:
            upload_url = f"{url}/storage/v1/object/{BUCKET_NAME}/{safe_filename}"
            response = requests.post(upload_url, headers=headers, data=f)
            if response.status_code != 200:
                print(f"Detalle del error de Supabase: {response.text}")
            response.raise_for_status()
        
        # Obtener la URL pública
        public_url = f"{url}/storage/v1/object/public/{BUCKET_NAME}/{safe_filename}"
        return public_url, file_mime, uploaded_file_path
    except Exception as e:
        raise RuntimeError(f"Error subiendo a Supabase Storage: {e}")
