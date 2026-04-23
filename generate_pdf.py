from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'WarrantyCentral - Resumen Ejecutivo', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

def create_executive_pdf():
    pdf = PDF()
    pdf.add_page()
    
    # Titulo
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Proyecto: MVP de Gestion de Garantias', 0, 1)
    pdf.ln(5)
    
    # Arquitectura
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, '1. Arquitectura del Sistema', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 8, 'El sistema ha sido estructurado en una arquitectura modular en Python. Se integro la solucion en la nube Supabase como backend principal para base de datos (PostgreSQL) y almacenamiento seguro de documentos (Supabase Storage).')
    pdf.ln(5)

    # Componentes
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, '2. Componentes Clave', 0, 1)
    pdf.set_font('Arial', '', 11)
    
    componentes = [
        "- Base de Datos (Supabase): Almacena Usuarios, Productos y Documentos.",
        "- OCR y Procesamiento: Extraccion de fechas de boletas usando Tesseract.",
        "- Logica de Garantias: Calculo automatico de vencimientos y enlaces a manuales.",
        "- Seguridad: Validacion estricta de Magic Bytes (tipos MIME) y peso maximo de 5MB.",
        "- Sistema de Alertas: Filtro automatizado de garantias a vencer en 30 dias."
    ]
    
    for comp in componentes:
        pdf.multi_cell(0, 8, comp)
        
    pdf.ln(5)
    
    # Estructura del Proyecto
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, '3. Estructura del Directorio Limpio', 0, 1)
    pdf.set_font('Courier', '', 10)
    
    estructura = """
proyecto-5/
├── alerts/
│   └── notifier.py        (Consultas de alertas a Supabase)
├── db/
│   └── supabase_client.py (Conexion REST a Supabase)
├── logic/
│   └── warranty.py        (Logica de negocio)
├── ocr/
│   └── processor.py       (Regex y extraccion OCR)
├── security/
│   └── validator.py       (Validacion de archivos y Storage)
├── main.py                (Orquestador del flujo MVP)
├── requirements.txt       (Dependencias de Python)
├── schema.sql             (Estructura SQL de Supabase)
└── .env                   (Credenciales seguras)
    """
    pdf.multi_cell(0, 5, estructura)
    
    # Guardar
    pdf_path = 'Resumen_Ejecutivo_WarrantyCentral.pdf'
    pdf.output(pdf_path, 'F')
    print(f"PDF generado exitosamente en: {pdf_path}")

if __name__ == '__main__':
    create_executive_pdf()
