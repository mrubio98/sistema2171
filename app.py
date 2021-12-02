#Elimine comentarios de la clase32
from flask import Flask
#importamos url_for y flash (flash es para validaciones)
from flask import render_template , request , redirect, url_for, flash
from flaskext.mysql import MySQL
from pymysql import DATETIME, cursors
from datetime import date, datetime
import os
from werkzeug.utils import send_from_directory

app = Flask(__name__)
#necesario para el flask
app.secret_key="Codoacodo"

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sistema2171' 
mysql.init_app(app)

CARPETA = os.path.join('uploads')
app.config['CARPETA'] = CARPETA

@app.route('/')
def index():
    sql="SELECT * FROM `empleados`"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)

    empleados = cursor.fetchall()
    conn.commit()

    return render_template('empleados/index.html', empleados = empleados)

@app.route('/create')
def create():
    return render_template('empleados/form.html')

@app.route('/store' , methods=['POST'])
def storage():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']

    #validaciones
    if _nombre == '' or _correo ==  '':
        flash('Falta llenar algun dato')
        return redirect(url_for('create'))

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%D")
    #modifique el string xq no me permitia guardar
    tiempo2 = tiempo.split('/')
    tiempo = ''.join(tiempo2)

    if _foto.filename != '':
        nuevoNombreFoto = tiempo + _foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)

    sql="INSERT INTO `empleados` (`id`, `nombre`, `mail`, `foto`) VALUES (NULL, %s, %s, %s);"
    datos =(_nombre,_correo,nuevoNombreFoto)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)

    cursor.execute("SELECT * FROM `empleados`")
    empleados = cursor.fetchall()
    conn.commit()

    return render_template('empleados/index.html', empleados = empleados)

@app.route('/delete/<int:id>')
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empleados WHERE id = %s", (id))

    try:
        #Eliminamos la foto
        cursor.execute("SELECT foto FROM empleados WHERE id = %s", (id))
        fotoVieja = cursor.fetchall()
        os.remove(os.path.join(app.config['CARPETA'], fotoVieja[0][0]))
    except:
        print("no pudo eliminar la foto")

    conn.commit()
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empleados WHERE id = %s", (id))
    empleados = cursor.fetchall()
    conn.commit()

    return render_template('empleados/edit.html', empleados = empleados)

@app.route('/update/<int:id>', methods = ['POST'])
def update(id):
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    _id = id

    conn = mysql.connect()
    cursor = conn.cursor()

    if _foto.filename != '':
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%D")
         #modifique el string xq no me permitia guardar
        tiempo2 = tiempo.split('/')
        tiempo = ''.join(tiempo2)

        nuevoNombreFoto = tiempo + _foto.filename
        _foto.save("uploads/"+ nuevoNombreFoto)

        cursor.excecute("SELECT foto FROM empleados WHERE id = %s", (id))
        fotoVieja = cursor.fetchall()
        os.remove(os.path.join(app.config['CARPETA'], fotoVieja[0][0]))

        sql = "UPDATE empleados SET foto=%s WHERE id =%s"
        datos =(nuevoNombreFoto,id)


    sql = "UPDATE empleados SET nombre = %s , mail=%s WHERE id =%s"
    datos =(_nombre,_correo,id)
    
    cursor.execute(sql, datos)
    conn.commit()

    return render_template('empleados/index.html')

#fotos
app.route('uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)


if __name__ == "__main__":
    app.run(debug=True)


#en la terminal escribir python app.py para arrancar
#se 'mata' la terminal con ctrl + c

#http://localhost:8080/phpmyadmin/ para ingresar en myadmin