import re
import pytesseract
from PIL import Image

def extract_receipt_data(image_path):
    """
    Toma una ruta de imagen de una boleta, extrae el texto usando OCR,
    y utiliza expresiones regulares para encontrar la fecha de compra y
    posibles nombres de productos.
    """
    try:
        # Extraer texto de la imagen
        text = pytesseract.image_to_string(Image.open(image_path), lang='spa+eng')
        
        # Expresión regular para buscar fechas en formatos comunes: DD/MM/YYYY o DD-MM-YYYY
        date_pattern = r'\b(0?[1-9]|[12][0-9]|3[01])[- /.](0?[1-9]|1[012])[- /.](19|20)\d\d\b'
        dates_found = re.findall(date_pattern, text)
        
        # Reconstruir la primera fecha encontrada a formato YYYY-MM-DD
        purchase_date = None
        if dates_found:
            day, month, year = dates_found[0]
            # Normalizar a dos dígitos para día y mes
            day = day.zfill(2)
            month = month.zfill(2)
            purchase_date = f"{year}-{month}-{day}"

        # Heurística simple para encontrar nombres de productos
        # En una aplicación real, se usaría NLP o Named Entity Recognition (NER).
        # Aquí buscamos líneas que tengan letras y números (común en modelos de productos)
        product_name = "Producto Desconocido"
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            # Ignorar líneas muy cortas, fechas, o palabras comunes
            if len(line) > 5 and re.search(r'[A-Za-z]', line) and re.search(r'[0-9]', line):
                # Filtramos líneas que parecen ser totales, ruts, etc.
                if not re.search(r'(total|rut|iva|tarjeta|efectivo)', line.lower()):
                    product_name = line
                    break

        return {
            "fecha_compra": purchase_date,
            "nombre_producto": product_name,
            "texto_completo": text
        }

    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        return None
