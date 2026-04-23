import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Faltan las variables de entorno SUPABASE_URL y SUPABASE_KEY")

supabase: Client = create_client(url, key)

def get_client() -> Client:
    return supabase

def insert_product(usuario_id: str, nombre_comercial: str, fecha_compra: str, meses_garantia: int, link_manual_pdf: str, fecha_vencimiento: str):
    """Inserta un producto en Supabase."""
    data = {
        "usuario_id": usuario_id,
        "nombre_comercial": nombre_comercial,
        "fecha_compra": fecha_compra,
        "meses_garantia": meses_garantia,
        "link_manual_pdf": link_manual_pdf,
        "fecha_vencimiento": fecha_vencimiento
    }
    response = supabase.table("productos").insert(data).execute()
    return response.data[0]['id']

def insert_document(producto_id: str, ruta_archivo: str, tipo_mime: str):
    """Inserta un registro de documento en Supabase."""
    data = {
        "producto_id": producto_id,
        "ruta_archivo": ruta_archivo,
        "tipo_mime": tipo_mime
    }
    response = supabase.table("documentos").insert(data).execute()
    return response.data[0]['id']
