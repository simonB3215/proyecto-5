import os
import shutil
from dotenv import load_dotenv
from db.supabase_client import get_client, insert_product, insert_document
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
    """Crea un usuario de prueba si no existe en Supabase."""
    supabase = get_client()
    email = 'test@example.com'
    
    # Verificar si existe
    response = supabase.table('usuarios').select('id').eq('email', email).execute()
    if response.data:
        return response.data[0]['id']
        
    # Crear si no existe
    response = supabase.table('usuarios').insert({
        'email': email,
        'nombre': 'Usuario Prueba'
    }).execute()
    return response.data[0]['id']

def process_receipt(usuario_id, receipt_image_path, meses_garantia=12):
    print(f"\n--- Procesando boleta: {receipt_image_path} ---")
    
    # 1. Simular subida (lo guardamos en temp_upload)
    temp_upload_path = mock_upload_file(receipt_image_path)
    if not temp_upload_path:
        return
        
    try:
        # 2. Seguridad: Validar archivo y subir a Supabase Storage
        print("Validando y subiendo archivo a Supabase Storage...")
        public_url, mime_type, original_temp_file = validate_and_save_file(temp_upload_path)
        print(f"Archivo subido. URL Pública: {public_url}")
        
        # 3. Procesamiento OCR (usamos el archivo temporal que aún existe localmente)
        print("Ejecutando OCR...")
        ocr_data = extract_receipt_data(original_temp_file)
        
        if ocr_data and ocr_data.get('fecha_compra'):
            fecha_compra = ocr_data['fecha_compra']
            nombre_producto = ocr_data['nombre_producto']
            print(f"Datos extraídos - Fecha: {fecha_compra}, Producto: {nombre_producto}")
            
            # 4. Lógica de Negocio
            fecha_vencimiento = calculate_expiration_date(fecha_compra, meses_garantia)
            link_manual = generate_manual_search_link(nombre_producto)
            print(f"Fecha de vencimiento calculada: {fecha_vencimiento}")
            print(f"Link a manual: {link_manual}")
            
            # 5. Base de Datos (Supabase)
            print("Guardando en la base de datos Supabase...")
            producto_id = insert_product(usuario_id, nombre_producto, fecha_compra, meses_garantia, link_manual, fecha_vencimiento)
            insert_document(producto_id, public_url, mime_type)
            print(f"Registro guardado con éxito! ID Producto: {producto_id}")
            
        else:
            print("No se pudo extraer la fecha de compra mediante OCR.")
            
    except Exception as e:
        print(f"Error en el proceso: {e}")
        
    finally:
        # Limpiar temp
        if temp_upload_path and os.path.exists(temp_upload_path):
            os.remove(temp_upload_path)

if __name__ == '__main__':
    print("Inicializando sistema WarrantyCentral MVP (Supabase Version)...")
    
    try:
        # Crear usuario de prueba
        usuario_id = create_mock_user()
        
        print("\n--- Para probar el flujo completo, necesitas proporcionar una imagen de recibo real ---")
        print("Como esto es un backend, invoca 'process_receipt(usuario_id, \"ruta_a_tu_boleta.jpg\")' dentro de main.py")
        
        print("\nEjecutando revisión de alertas:")
        run_alert_check()
    except Exception as e:
        print(f"Error de inicialización: {e}")
        print("Asegúrate de haber configurado tu archivo .env y ejecutado el schema.sql en Supabase.")
