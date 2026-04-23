import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'warranty.db')

def get_connection():
    """Retorna una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa la base de datos y crea las tablas necesarias."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tabla Usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        nombre TEXT NOT NULL,
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Tabla Productos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        nombre_comercial TEXT NOT NULL,
        fecha_compra DATE NOT NULL,
        meses_garantia INTEGER NOT NULL,
        link_manual_pdf TEXT,
        fecha_vencimiento DATE NOT NULL,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )
    ''')

    # Tabla Documentos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS documentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto_id INTEGER,
        ruta_archivo TEXT NOT NULL,
        tipo_mime TEXT NOT NULL,
        fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(producto_id) REFERENCES productos(id)
    )
    ''')

    conn.commit()
    conn.close()

def insert_product(usuario_id, nombre_comercial, fecha_compra, meses_garantia, link_manual_pdf, fecha_vencimiento):
    """Inserta un producto en la base de datos y retorna su ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO productos (usuario_id, nombre_comercial, fecha_compra, meses_garantia, link_manual_pdf, fecha_vencimiento)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (usuario_id, nombre_comercial, fecha_compra, meses_garantia, link_manual_pdf, fecha_vencimiento))
    product_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return product_id

def insert_document(producto_id, ruta_archivo, tipo_mime):
    """Inserta un registro de documento."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO documentos (producto_id, ruta_archivo, tipo_mime)
        VALUES (?, ?, ?)
    ''', (producto_id, ruta_archivo, tipo_mime))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Base de datos inicializada correctamente.")
