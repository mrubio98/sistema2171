#El nombre del archivo debe ser app.py

#importar flask
from flask import Flask
from flask import render_template , request

#importar de flask la libreria de base de datos
from flaskext.mysql import MySQL
from pymysql import cursors

app = Flask(__name__)

#crear ruta con base de datos
mysql = MySQL()
#configurar los datos del database
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sistema2171' #nombre de la base de dato
#iniciar
mysql.init_app(app)

#crear ruta
@app.route('/')
def index():
    #base de datos
    sql="INSERT INTO `empleados` (`id`, `nombre`, `mail`, `foto`) VALUES (NULL, 'tuki', 'tukicapo@ciudad.com.ar', 'fotodetuki.jpg');"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

    #ruta
    return render_template('empleados/index.html')

@app.route('/create')
def create():
    return render_template('empleados/form.html')

@app.route('/store' , methods=['POST'])
def storage():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']

    sql="INSERT INTO `empleados` (`id`, `nombre`, `mail`, `foto`) VALUES (NULL, %s, %s, %s);"
    datos =(_nombre,_correo,_foto.filename)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return render_template('empleados/index.html')

    


if __name__ == "__main__":
    app.run(debug=True)

#en la terminal escribir python app.py para arrancar
#se 'mata' la terminal con ctrl + c



#http://localhost:8080/phpmyadmin/ para ingresar en myadmin