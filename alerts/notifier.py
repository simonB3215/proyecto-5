from db.database import get_connection
from datetime import datetime
import json

def get_expiring_warranties(days=30):
    """
    Busca en la base de datos los productos cuyas garantías
    vencen en los próximos 'days' días.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Consultar productos que vencen entre hoy y hoy + days
    query = f'''
        SELECT p.id, p.nombre_comercial, p.fecha_vencimiento, u.email as usuario_email, u.nombre as usuario_nombre
        FROM productos p
        JOIN usuarios u ON p.usuario_id = u.id
        WHERE p.fecha_vencimiento BETWEEN DATE('now') AND DATE('now', '+{days} days')
        ORDER BY p.fecha_vencimiento ASC
    '''
    
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    
    expiring_products = []
    for row in rows:
        expiring_products.append(dict(row))
        
    return expiring_products

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
        print(f"[ALERTA] El producto '{product['nombre_comercial']}' "
              f"del usuario {product['usuario_nombre']} "
              f"vencerá el {product['fecha_vencimiento']}.")
              
    return expiring

if __name__ == "__main__":
    run_alert_check()
