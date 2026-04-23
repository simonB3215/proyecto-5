import os
import requests
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL", "").rstrip('/')
key: str = os.environ.get("SUPABASE_KEY", "")

if not url or not key:
    raise ValueError("Faltan las variables de entorno SUPABASE_URL y SUPABASE_KEY")

headers = {
    "apikey": key,
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def get_base_url():
    return url

def get_headers():
    return headers

def insert_product(usuario_id: str, nombre_comercial: str, fecha_compra: str, meses_garantia: int, link_manual_pdf: str, fecha_vencimiento: str):
    """Inserta un producto en Supabase usando REST."""
    data = {
        "usuario_id": usuario_id,
        "nombre_comercial": nombre_comercial,
        "fecha_compra": fecha_compra,
        "meses_garantia": meses_garantia,
        "link_manual_pdf": link_manual_pdf,
        "fecha_vencimiento": fecha_vencimiento
    }
    
    response = requests.post(f"{url}/rest/v1/productos", headers=headers, json=data)
    response.raise_for_status()
    return response.json()[0]['id']

def insert_document(producto_id: str, ruta_archivo: str, tipo_mime: str):
    """Inserta un registro de documento en Supabase usando REST."""
    data = {
        "producto_id": producto_id,
        "ruta_archivo": ruta_archivo,
        "tipo_mime": tipo_mime
    }
    response = requests.post(f"{url}/rest/v1/documentos", headers=headers, json=data)
    response.raise_for_status()
    return response.json()[0]['id']
