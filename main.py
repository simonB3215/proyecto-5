import os
import shutil
import requests
from dotenv import load_dotenv
from db.supabase_client import get_base_url, get_headers, insert_product, insert_document
from ocr.processor import extract_receipt_data
from logic.warranty import calculate_expiration_date, generate_manual_search_link
from alerts.notifier import run_alert_check
from security.validator import validate_and_save_file

load_dotenv()

def mock_upload_file(source_path, temp_dest="temp_upload"):
    """Simula la subida de un archivo temporalmente al servidor."""
    if not os.path.exists(source_path):
        print(f"El archivo {source_path} no existe para la simulación.")
        return None
    
    if not os.path.exists(temp_dest):
        os.makedirs(temp_dest)
        
    filename = os.path.basename(source_path)
    temp_path = os.path.join(temp_dest, filename)
    shutil.copy2(source_path, temp_path)
    return temp_path

def create_mock_user():
    """Crea un usuario de prueba si no existe en Supabase usando REST."""
    url = get_base_url()
    headers = get_headers()
    email = 'test@example.com'
    
    # Verificar si existe
    response = requests.get(f"{url}/rest/v1/usuarios?email=eq.{email}&select=id", headers=headers)
    response.raise_for_status()
    data = response.json()
    if data:
        return data[0]['id']
        
    # Crear si no existe
    create_res = requests.post(f"{url}/rest/v1/usuarios", headers=headers, json={
        'email': email,
        'nombre': 'Usuario Prueba'
    })
    create_res.raise_for_status()
    return create_res.json()[0]['id']

def process_receipt(usuario_id, receipt_image_path, meses_garantia=12):
    print(f"\n--- Procesando boleta: {receipt_image_path} ---")
    
    temp_upload_path = mock_upload_file(receipt_image_path)
    if not temp_upload_path:
        return
        
    try:
        print("Validando y subiendo archivo a Supabase Storage...")
        public_url, mime_type, original_temp_file = validate_and_save_file(temp_upload_path)
        print(f"Archivo subido. URL Pública: {public_url}")
        
        print("Ejecutando OCR...")
        ocr_data = extract_receipt_data(original_temp_file)
        
        if ocr_data and ocr_data.get('fecha_compra'):
            fecha_compra = ocr_data['fecha_compra']
            nombre_producto = ocr_data['nombre_producto']
            print(f"Datos extraídos - Fecha: {fecha_compra}, Producto: {nombre_producto}")
            
            fecha_vencimiento = calculate_expiration_date(fecha_compra, meses_garantia)
            link_manual = generate_manual_search_link(nombre_producto)
            print(f"Fecha de vencimiento calculada: {fecha_vencimiento}")
            print(f"Link a manual: {link_manual}")
            
            print("Guardando en la base de datos Supabase...")
            producto_id = insert_product(usuario_id, nombre_producto, fecha_compra, meses_garantia, link_manual, fecha_vencimiento)
            insert_document(producto_id, public_url, mime_type)
            print(f"Registro guardado con éxito! ID Producto: {producto_id}")
            
        else:
            print("No se pudo extraer la fecha de compra mediante OCR.")
            
    except Exception as e:
        print(f"Error en el proceso: {e}")
        
    finally:
        if temp_upload_path and os.path.exists(temp_upload_path):
            os.remove(temp_upload_path)

if __name__ == '__main__':
    print("Inicializando sistema WarrantyCentral MVP (Supabase REST Version)...")
    
    try:
        usuario_id = create_mock_user()
        
        # --- AQUI PONES TU FOTO ---
        # 1. Pega tu foto en la carpeta proyecto-5
        # 2. Cambia "tu_foto_aqui.jpg" por el nombre real de tu foto
        # 3. Quita el '#' del principio de la siguiente linea para descomentarla y activarla:
        
        process_receipt(usuario_id, "1.jpg")
        
        print("\nEjecutando revisión de alertas:")
        run_alert_check()
    except Exception as e:
        print(f"Error de inicialización: {e}")
        print("Asegúrate de haber configurado tu archivo .env y ejecutado el schema.sql en Supabase.")
