import os
import uuid
import magic  # python-magic

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

def validate_and_save_file(uploaded_file_path, dest_folder="uploads"):
    """
    Valida un archivo subido por:
    1. Tamaño.
    2. Extensión.
    3. Tipo MIME real usando libmagic.
    
    Si es válido, lo mueve a la carpeta destino renombrándolo con un UUID seguro.
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

    # Crear carpeta destino si no existe
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # 4. Generar nombre seguro (UUID)
    safe_filename = f"{uuid.uuid4()}{ext}"
    final_path = os.path.join(dest_folder, safe_filename)

    # En un entorno real (ej. Flask), aquí guardaríamos el FileStorage.
    # Para el MVP, simplemente renombramos/movemos el archivo temporal
    # asumiendo que 'uploaded_file_path' es la ruta temporal donde se subió.
    
    # os.rename(uploaded_file_path, final_path) # Comentado para MVP de consola
    
    return final_path, file_mime
