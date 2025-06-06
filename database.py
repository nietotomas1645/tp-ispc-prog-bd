import pyodbc
import re
import hashlib

def check_database():
    try:
        conn = pyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=localhost\\SQLEXPRESS;"
            "Database=master;"
            "Trusted_Connection=yes;"
            "Encrypt=yes;"
            "TrustServerCertificate=yes;",
            autocommit=True
        )
        cursor = conn.cursor()
        cursor.execute("IF DB_ID('crudUsers') IS NULL BEGIN CREATE DATABASE crudUsers END")
        print(" Base de datos verificada o creada.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f" Error al crear/verificar base de datos: {e}")

def get_connection():
    try:
        return pyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=localhost\\SQLEXPRESS;"
            "Database=crudUsers;"
            "Trusted_Connection=yes;"
            "Encrypt=yes;"
            "TrustServerCertificate=yes;"
        )
    except Exception as e:
        print(f" Error de conexión: {e}")
        return None

def create_user_table():
    conn = get_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Usuarios' AND xtype='U')
        CREATE TABLE Usuarios (
            Id INT PRIMARY KEY IDENTITY,
            Nombre NVARCHAR(100),
            Usuario NVARCHAR(50) UNIQUE,
            Contrasena NVARCHAR(100),
            Rol NVARCHAR(20)
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_password(password):
    return len(password) >= 6 and re.search(r"[a-zA-Z]", password) and re.search(r"\d", password)

def add_user(name, username, password, role):
    if not name.strip() or not username.strip():
        print(" El nombre y el usuario no pueden estar vacíos.")
        return

    if role not in ["admin", "usuario"]:
        print(" Rol inválido. Debe ser 'admin' o 'usuario'.")
        return

    if not is_valid_password(password):
        print(" La contraseña debe tener al menos 6 caracteres, incluyendo letras y números.")
        return

    conn = get_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        hashed = hash_password(password)
        cursor.execute('''
            INSERT INTO Usuarios (Nombre, Usuario, Contrasena, Rol)
            VALUES (?, ?, ?, ?)
        ''', (name.strip(), username.strip(), hashed, role))
        conn.commit()
        print(" Usuario registrado con éxito.")
    except pyodbc.IntegrityError:
        print(" El nombre de usuario ya existe. Intenta con otro.")
    except Exception as e:
        print(f" Error: {e}")
    finally:
        cursor.close()
        conn.close()

def login_user(username, password):
    conn = get_connection()
    if conn is None:
        return None
    cursor = conn.cursor()
    hashed = hash_password(password)
    cursor.execute('''
        SELECT Nombre, Usuario, Rol FROM Usuarios
        WHERE Usuario = ? AND Contrasena = ?
    ''', (username.strip(), hashed))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return {"name": result[0], "username": result[1], "role": result[2]}
    else:
        return None

def list_users():
    conn = get_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute('SELECT Id, Nombre, Usuario, Rol FROM Usuarios')
    users = cursor.fetchall()
    print("\n Lista de usuarios:")
    for u in users:
        print(f"ID: {u[0]} | Nombre: {u[1]} | Usuario: {u[2]} | Rol: {u[3]}")
    cursor.close()
    conn.close()

def delete_user_by_id(user_id):
    conn = get_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Usuarios WHERE Id = ?', (int(user_id),))
    if cursor.rowcount > 0:
        print(" Usuario eliminado.")
    else:
        print(" Usuario no encontrado.")
    conn.commit()
    cursor.close()
    conn.close()
