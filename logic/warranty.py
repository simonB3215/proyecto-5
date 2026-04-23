from datetime import datetime
from dateutil.relativedelta import relativedelta
import urllib.parse

def calculate_expiration_date(purchase_date_str, warranty_months):
    """
    Calcula la fecha de vencimiento sumando los meses de garantía a la fecha de compra.
    """
    try:
        purchase_date = datetime.strptime(purchase_date_str, "%Y-%m-%d").date()
        expiration_date = purchase_date + relativedelta(months=warranty_months)
        return expiration_date.strftime("%Y-%m-%d")
    except ValueError as e:
        print(f"Error de formato de fecha: {e}")
        return None

def generate_manual_search_link(product_name):
    """
    Genera un enlace de búsqueda de Google automatizado para encontrar
    el manual del producto en formato PDF.
    """
    # Limpiar el nombre del producto para la URL
    clean_name = product_name.strip()
    query = f"{clean_name} manual filetype:pdf"
    
    # Codificar la consulta para la URL
    url_encoded_query = urllib.parse.quote_plus(query)
    search_url = f"https://www.google.com/search?q={url_encoded_query}"
    
    return search_url
