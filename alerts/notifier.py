from db.supabase_client import get_client
from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_expiring_warranties(days=30):
    """
    Busca en Supabase los productos cuyas garantías
    vencen en los próximos 'days' días.
    """
    supabase = get_client()
    
    hoy = datetime.now().strftime('%Y-%m-%d')
    fecha_limite = (datetime.now() + relativedelta(days=days)).strftime('%Y-%m-%d')
    
    # Consultar productos que vencen entre hoy y la fecha límite
    # Nota: Supabase select no hace JOIN automático sin foreign key bien definida o usar sintaxis de join de postgrest.
    # Usaremos una consulta anidada para traer los datos del usuario.
    try:
        response = supabase.table('productos').select(
            'id, nombre_comercial, fecha_vencimiento, usuarios(email, nombre)'
        ).gte('fecha_vencimiento', hoy).lte('fecha_vencimiento', fecha_limite).execute()
        
        return response.data
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
