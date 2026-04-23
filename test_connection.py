import requests
from db.supabase_client import get_base_url, get_headers

url = get_base_url()
headers = get_headers()

try:
    # Intenta hacer una consulta simple a la tabla usuarios
    response = requests.get(f"{url}/rest/v1/usuarios?select=*", headers=headers)
    response.raise_for_status()
    print("¡Conexión exitosa a Supabase (REST)!")
    print(f"Respuesta ({len(response.json())} usuarios encontrados): {response.json()}")
except requests.exceptions.RequestException as e:
    print(f"Error de conexión: {e}")
