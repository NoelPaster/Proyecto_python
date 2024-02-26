from collections import UserString
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, session
from valid_form import valid_form

app = Flask(__name__)
app.secret_key = "blog_key"

def get_db_connection():
    conn = sqlite3.connect('proyecto_python.db')
    cursor = conn.cursor()
    return conn, cursor


#Ruta donde visualizar todos los post y  poder buscarlos por titulo con sqlite
@app.route('/')
def home():
    conn, cursor = get_db_connection()
    buscar= request.args.get("search")
    if buscar:
        cursor.execute("SELECT * FROM posts WHERE posts.titulo LIKE ?" , (f"%{buscar}%",))
        posts = cursor.fetchall()
        conn.close
        return render_template("home.html" , nombre = "Maria Noel Paster Mercedes" , posts=posts)
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    conn.close
    return render_template("home.html" , nombre = "Maria Noel Paster Mercedes" , posts=posts)


#Ruta estatica a info del blog
@app.route('/acerca_de')
def acerca_de():
    return render_template("acerca_de.html", nombre="Maria Noel Paster Mercedes")


#Ruta para visualizar post por id con sqlite
@app.route('/post/<id>')
def post_id(id):
    conn, cursor = get_db_connection()
    cursor.execute("SELECT * FROM posts WHERE posts.id == ?" , id)
    post = cursor.fetchone()
    conn.close()
    return render_template("post.html" , nombre = "Maria Noel Paster Mercedes" , post=post)


#Ruta para login con sqlite. El metodo get nos muestra el formulario y el metodo post procesa los datos ingresados
@app.route('/login', methods= ["GET" , "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", nombre="Maria Noel Paster Mercedes")
    elif request.method == "POST":            
        username = request.form["username"]
        password = request.form["password"]
        conn, cursor = get_db_connection()
        cursor.execute("SELECT * FROM users WHERE users.username == ?",(username,))
        user_exist = cursor.fetchone()
        conn.close()
        if user_exist and user_exist[2] == password :
            session['username'] = username
            return redirect('/')
        else:
            return render_template("login.html" , nombre = "Maria Noel Paster Mercedes" , error= "Usuario o contraseña incorrecto")


#Ruta para registrar un usuario nuevo con sqlite
@app.route('/register' , methods=["GET" , "POST"])
def new_user():
    if request.method == "GET":
        return render_template("register.html" , nombre="Maria Noel Paster Mercedes")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not valid_form(username=username , password=password):
            return render_template("register.html", nombre = "Maria Noel Paster Mercedes", error="Ocurrio un error. Valide sus datos nuevamente")

        conn, cursor = get_db_connection()
        cursor.execute("SELECT * FROM users WHERE users.username == ?",(username,))
        user_exist = cursor.fetchone()
        if user_exist:
            return render_template("register.html" , nombre="Maria Noel Paster Mercedes" , error = "El usuario ya existe") 

        cursor.execute("INSERT INTO users (username , password) VALUES (? , ?)" , (username , password))
        conn.commit()
        conn.close()
    return redirect('/login')


#Ruta para crear un nuevo post con sqlite.   
@app.route('/nuevo_post' , methods=["GET" , "POST"])
def nuevo_post():
    if request.method == "GET":
        username = session.get("username")
        if not username:
            return render_template("login.html" , error = "Debe de inciar sesión")
        return render_template("nuevo_post.html" , nombre="Maria Noel Paster Mercedes")
    elif request.method == "POST":
        username = session.get("username")
        autor = username
        titulo = request.form["titulo"]
        comentario = request.form["comentario"]
        if autor and titulo and comentario:
            conn, cursor = get_db_connection()
            cursor.execute("INSERT INTO posts (autor , titulo , comentario) VALUES (? , ? , ?)" , (autor , titulo , comentario))
            conn.commit()
            conn.close()
            return redirect('/')
        else:
            return render_template("nuevo_post.html" , nombre="Maria Noel Paster Mercedes" , error= "Todos los campos son obligatorios")


#Ruta para cerrar sesion
@app.route('/logout')
def logout():
    username = session.get("username")
    if not username:
        return render_template("login.html" , error="Debe de iniciar sesión")
    session.pop("username",None)
    return redirect('/')

app.run(debug=True)