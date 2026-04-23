import os
import uuid
import magic
from db.supabase_client import get_client

# Extensiones permitidas (MVP)
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.pdf'}

# Tipos MIME permitidos
ALLOWED_MIMES = {
    'image/jpeg',
    'image/png',
    'application/pdf'
}

# Límite de tamaño: 5MB
MAX_FILE_SIZE = 5 * 1024 * 1024

BUCKET_NAME = "documentos_garantia"

def validate_and_save_file(uploaded_file_path):
    """
    Valida un archivo subido y lo sube al Storage de Supabase.
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

    # 3. Verificar MIME type real (protección contra renombramiento de extensiones)
    mime = magic.Magic(mime=True)
    file_mime = mime.from_file(uploaded_file_path)
    if file_mime not in ALLOWED_MIMES:
        raise ValueError(f"Tipo MIME no permitido: {file_mime}")

    # 4. Generar nombre seguro (UUID)
    safe_filename = f"{uuid.uuid4()}{ext}"

    # 5. Subir a Supabase Storage
    supabase = get_client()
    try:
        with open(uploaded_file_path, 'rb') as f:
            supabase.storage.from_(BUCKET_NAME).upload(
                path=safe_filename,
                file=f,
                file_options={"content-type": file_mime}
            )
        
        # Obtener la URL pública
        public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(safe_filename)
        return public_url, file_mime, uploaded_file_path
    except Exception as e:
        raise RuntimeError(f"Error subiendo a Supabase Storage: {e}")
