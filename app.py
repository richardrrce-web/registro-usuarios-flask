from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Función auxiliar para conectarnos a la base de datos de forma segura
def conectar_bd():
    conexion = sqlite3.connect('usuarios.db')
    # Permite acceder a las columnas por su nombre
    conexion.row_factory = sqlite3.Row 
    return conexion

# Crear la tabla en la Base de Datos al arrancar la app si no existe
def inicializar_bd():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    # Creamos una tabla llamada 'registros' con un ID, un Nombre y la Fecha
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conexion.commit()
    conexion.close()

# Ejecutamos la creación de la base de datos
inicializar_bd()

# 1. RUTA PRINCIPAL: Muestra el formulario HTML
@app.route('/')
def inicio():
    return render_template('index.html')

# 2. RUTA PARA RECIBIR Y GUARDAR DATOS
@app.route('/enviar', methods=['POST'])
def enviar_datos():
    if request.method == 'POST':
        nombre = request.form.get('nombre_usuario')
        
        # Guardamos en la Base de Datos
        conexion = conectar_bd()
        cursor = conexion.cursor()
        cursor.execute('INSERT INTO registros (nombre) VALUES (?)', (nombre,))
        conexion.commit()
        conexion.close()
        
        # Redirigimos a la página que muestra la lista de nombres
        return redirect(url_for('ver_usuarios'))

# 3. RUTA NUEVA: Muestra todos los usuarios registrados
@app.route('/usuarios')
def ver_usuarios():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    # Leemos todos los registros guardados
    cursor.execute('SELECT * FROM registros ORDER BY fecha DESC')
    lista_usuarios = cursor.fetchall()
    conexion.close()
    
    # Le pasamos la lista de usuarios a una nueva plantilla HTML
    return render_template('usuarios.html', usuarios=lista_usuarios)

if __name__ == '__main__':
    app.run(debug=True)