import os
import shutil
from db.database import init_db, insert_product, insert_document, get_connection
from ocr.processor import extract_receipt_data
from logic.warranty import calculate_expiration_date, generate_manual_search_link
from alerts.notifier import run_alert_check
from security.validator import validate_and_save_file

def mock_upload_file(source_path, temp_dest="temp_upload"):
    """
    Simula la subida de un archivo al servidor.
    """
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
    """Crea un usuario de prueba si no existe."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (email, nombre) VALUES ('test@example.com', 'Usuario Prueba')")
        conn.commit()
        user_id = cursor.lastrowid
    except:
        # Ya existe
        cursor.execute("SELECT id FROM usuarios WHERE email='test@example.com'")
        user_id = cursor.fetchone()['id']
    conn.close()
    return user_id

def process_receipt(usuario_id, receipt_image_path, meses_garantia=12):
    print(f"\n--- Procesando boleta: {receipt_image_path} ---")
    
    # 1. Simular subida
    temp_upload_path = mock_upload_file(receipt_image_path)
    if not temp_upload_path:
        return
        
    try:
        # 2. Seguridad: Validar archivo
        print("Validando archivo por seguridad...")
        final_file_path, mime_type = validate_and_save_file(temp_upload_path)
        # Movemos el archivo a uploads
        shutil.move(temp_upload_path, final_file_path)
        print(f"Archivo guardado de forma segura en: {final_file_path}")
        
        # 3. Procesamiento OCR
        print("Ejecutando OCR...")
        ocr_data = extract_receipt_data(final_file_path)
        
        if ocr_data and ocr_data.get('fecha_compra'):
            fecha_compra = ocr_data['fecha_compra']
            nombre_producto = ocr_data['nombre_producto']
            print(f"Datos extraídos - Fecha: {fecha_compra}, Producto: {nombre_producto}")
            
            # 4. Lógica de Negocio
            fecha_vencimiento = calculate_expiration_date(fecha_compra, meses_garantia)
            link_manual = generate_manual_search_link(nombre_producto)
            print(f"Fecha de vencimiento calculada: {fecha_vencimiento}")
            print(f"Link a manual: {link_manual}")
            
            # 5. Base de Datos
            print("Guardando en la base de datos...")
            producto_id = insert_product(usuario_id, nombre_producto, fecha_compra, meses_garantia, link_manual, fecha_vencimiento)
            insert_document(producto_id, final_file_path, mime_type)
            print(f"Registro guardado con éxito! ID Producto: {producto_id}")
            
        else:
            print("No se pudo extraer la fecha de compra mediante OCR.")
            
    except Exception as e:
        print(f"Error en el proceso: {e}")
        
    finally:
        # Limpiar temp si quedó algo
        if temp_upload_path and os.path.exists(temp_upload_path):
            os.remove(temp_upload_path)

if __name__ == '__main__':
    print("Inicializando sistema WarrantyCentral MVP...")
    # Inicializar DB
    init_db()
    
    # Crear usuario de prueba
    usuario_id = create_mock_user()
    
    print("\n--- Para probar el flujo completo, necesitas proporcionar una imagen de recibo real ---")
    print("Como esto es un backend, puedes ejecutar main.py e invocar 'process_receipt(usuario_id, \"ruta_a_tu_boleta.jpg\")'")
    print("\nEjecutando revisión de alertas (probablemente vacía inicialmente):")
    run_alert_check()
