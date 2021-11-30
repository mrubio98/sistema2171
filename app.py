#Elimine comentarios de la clase31
from flask import Flask
#incluimos redirect para redireccionar a la misma pagina
from flask import render_template , request , redirect
from flaskext.mysql import MySQL
from pymysql import DATETIME, cursors

#importamos datetime para insertarlo en las fotos para que no halla dos iguales
from datetime import date, datetime

#importarmos las librerias de sistema operativo
import os

app = Flask(__name__)


mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sistema2171' #nombre de la base de dato
mysql.init_app(app)

#hacemos referencia a la carpeta de uploads
CARPETA = os.path.join('uploads')
app.config['CARPETA'] = CARPETA

@app.route('/')
def index():
    #traemos los datos de empleados
    sql="SELECT * FROM `empleados`"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)

    #diferencia con insert
    empleados = cursor.fetchall()
    print(empleados)

    conn.commit()

    #enviamos ademas la lista empleados
    return render_template('empleados/index.html', empleados = empleados)

@app.route('/create')
def create():
    return render_template('empleados/form.html')

@app.route('/store' , methods=['POST'])
def storage():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']

    #pido la hora y la transformo en string
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%D")

    #chequeamos si envio la foto
    if _foto.filename != '':
        #creamos nuevo nombre
        nuevoNombreFoto = tiempo + _foto.filename
        #y guardamos
        _foto.save("uploads/"+ nuevoNombreFoto)

    sql="INSERT INTO `empleados` (`id`, `nombre`, `mail`, `foto`) VALUES (NULL, %s, %s, %s);"
    datos =(_nombre,_correo,nuevoNombreFoto)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return render_template('empleados/index.html')

#metodo para eliminar
#<int:id> captura un parametro int en la variable id
@app.route('/delete/<int:id>')
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empleados WHERE id = %s", (id))
    conn.commit()
    #usamos redirect ya que estamos usamos el mismo template - buena practica
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empleados WHERE id = %s", (id))

    #trae la data
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

    #foto
    if _foto.filename != '':
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%D")

        nuevoNombreFoto = tiempo + _foto.filename
        _foto.save("uploads/"+ nuevoNombreFoto)

        #borrar la foto vieja
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


if __name__ == "__main__":
    app.run(debug=True)



#en la terminal escribir python app.py para arrancar
#se 'mata' la terminal con ctrl + c

#http://localhost:8080/phpmyadmin/ para ingresar en myadmin