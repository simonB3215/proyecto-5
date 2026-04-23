import requests
from db.supabase_client import get_base_url, get_headers
from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_expiring_warranties(days=30):
    """
    Busca en Supabase (REST) los productos cuyas garantías
    vencen en los próximos 'days' días.
    """
    url = get_base_url()
    headers = get_headers()
    
    hoy = datetime.now().strftime('%Y-%m-%d')
    fecha_limite = (datetime.now() + relativedelta(days=days)).strftime('%Y-%m-%d')
    
    # Consultar productos. Usamos PostgREST select para hacer join con usuarios
    try:
        query_url = f"{url}/rest/v1/productos?select=id,nombre_comercial,fecha_vencimiento,usuarios(email,nombre)&fecha_vencimiento=gte.{hoy}&fecha_vencimiento=lte.{fecha_limite}"
        response = requests.get(query_url, headers=headers)
        response.raise_for_status()
        
        return response.json()
    except Exception as e:
        print(f"Error consultando Supabase: {e}")
        return []

def run_alert_check():
    """
    Ejecuta la revisión y retorna un log o envía un correo (mock).
    """
    print("--- Verificando Vencimientos de Garantías ---")
    expiring = get_expiring_warranties()
    
    if not expiring:
        print("No hay productos próximos a vencer.")
        return []
        
    for product in expiring:
        usuario_nombre = product.get('usuarios', {}).get('nombre', 'Desconocido')
        print(f"[ALERTA] El producto '{product['nombre_comercial']}' "
              f"del usuario {usuario_nombre} "
              f"vencerá el {product['fecha_vencimiento']}.")
              
    return expiring

if __name__ == "__main__":
    run_alert_check()
