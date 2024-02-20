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

#Falsa base de datos de posts
# posts= [
#    {"id": 1 , "usuario": "Maria" , "comentario": "comentario1" , "titulo": "titulo1"},
#    {"id": 2 , "usuario": "Noel" , "comentario": "comentario2" , "titulo": "titulo2"}
# ]

#Falsa base de datos de users
# users= [
#    {"username": "mnoel" , "password": "noel.1"},
#    {"username": "noelpaster" , "password": "123paster"}
# ]

#Ruta a home donde visualizar todos los posts con base de datos falsa
# @app.route('/')
# def home():
#     buscar= request.args.get("search")
#     if buscar:
#         # list_post=[]
#         # for post in posts:
#         #     if buscar.lower() in post["titulo"].lower():
#         #         list_post.append(post)
#         # return render_template("home.html", nombre="Maria", posts=list_post)
#     else:
#         return render_template("home.html", nombre="Maria", posts=posts)

#Ruta donde visualizar todos los post y  poder buscarlos por titulo con sqlite
@app.route('/')
def home():
    conn, cursor = get_db_connection()
    buscar= request.args.get("search")
    if buscar:
        cursor.execute("SELECT * FROM posts WHERE posts.titulo LIKE ?" , (f"%{buscar}%",))
        posts = cursor.fetchall()
        conn.close
        return render_template("home.html" , nombre = "Maria" , posts=posts)
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    conn.close
    return render_template("home.html" , nombre = "Maria" , posts=posts)


#Ruta estatica a info del blog
@app.route('/acerca_de')
def acerca_de():
    return render_template("acerca_de.html", nombre="Maria")


# #Ruta para visualizar post por id con base de datos falsa
# @app.route('/post/<int:id>')
# def post_id(id):
#     for post in posts:
#        if post["id"] == id:
#             return render_template("post.html", nombre="Maria", post = post)
#     return "ok"

#Ruta para visualizar post por id con sqlite
@app.route('/post/<id>')
def post_id(id):
    conn, cursor = get_db_connection()
    cursor.execute("SELECT * FROM posts WHERE posts.id == ?" , id)
    post = cursor.fetchone()
    conn.close()
    return render_template("post.html" , nombre = "Maria" , post=post)

#Ruta para login con base de datos falsa. El metodo get nos muestra el formulario y el metodo post procesa los datos ingresados
# @app.route('/login', methods= ["GET" , "POST"])
# def login():
#     if request.method == "GET":
#         return render_template("login.html", nombre="Maria")
#     elif request.method == "POST":
#         for user in users:
#             if user['username'] == request.form['username'] and user['password'] == request.form['password']:
#                 return 'login con exito'
#             else:
#                 return render_template("login.html" , error= "usuario o contrasena incorrecto")
        
        #print(request.form)
        #return redirect('/')

#Ruta para login con sqlite. El metodo get nos muestra el formulario y el metodo post procesa los datos ingresados
@app.route('/login', methods= ["GET" , "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", nombre="Maria")
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
            return render_template("login.html" , nombre = "Maria" , error= "Usuario o contrasena incorrecto")

#Ruta para registrar un usuario nuevo con base de datos falsa
# @app.route('/register' , methods=["GET" , "POST"])
# def register():
#     if request.method == "GET":
#         return render_template("register.html" , nombre="Maria")
#     elif request.method == "POST":
#             user_exist = list(filter(lambda user: user['username'] == request.form ['username'] , users))
#             if user_exist:
#                 return render_template("register.html" , nombre="Maria" , error = "El usuario ya esta registrado")
#             new_id = users[-1]["id"] +1
#             print(new_id)
#             new_user = {"id": new_id , "username": request.form['username'] , "pasword": request.form['password']}
#             users.append(new_user)
#             print(users)
#             return "ok"

#Ruta para registrar un usuario nuevo con sqlite
@app.route('/register' , methods=["GET" , "POST"])
def new_user():
    if request.method == "GET":
        return render_template("register.html" , nombre="Maria")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # if not username or not password:
        #     return render_template("register.html" , nombre="Maria" , error = "El username y password son obligatorios")
        
        # if len(password) < 6 : 
        #     return render_template("register.html" , nombre="Maria" , error = "Password debe contener al menos 6 caracteres")

        if not valid_form(username=username , password=password):
            return render_template("register.html", nombre = "Maria", error="Ocurrio un error. Valide sus datos nuevamente")

        conn, cursor = get_db_connection()
        cursor.execute("SELECT * FROM users WHERE users.username == ?",(username,))
        user_exist = cursor.fetchone()
        if user_exist:
            return render_template("register.html" , nombre="Maria" , error = "El usuario ya existe") 

        cursor.execute("INSERT INTO users (username , password) VALUES (? , ?)" , (username , password))
        conn.commit()
        conn.close()
    return redirect('/login')

# #Ruta para crear un nuevo post. El metodo get nos muestra el formulario y el metodo post procesa los datos ingresados
# @app.route('/nuevo_post', methods= ["GET" , "POST"])
# def nuevo_post():
#     if request.method == "GET":
#         return render_template("nuevo_post.html", nombre="Maria")
#     elif request.method == "POST":
#         print(request.form)
#         return "gracias por el nuevo post"

#Ruta para crear un nuevo post con sqlite.   
@app.route('/nuevo_post' , methods=["GET" , "POST"])
def nuevo_post():
    if request.method == "GET":
        username = session.get("username")
        if not username:
            return render_template("login.html" , error = "Debe de inciar sesion")
        return render_template("nuevo_post.html" , nombre="Maria")
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
            return render_template("nuevo_post.html" , nombre="Maria" , error= "Todos los campos son obligatorios")
   
@app.route('/logout')
def logout():
    username = session.get("username")
    if not username:
        return render_template("login.html" , error="Debe de iniciar sesion")
    session.pop("username",None)
    return redirect('/')

app.run(debug=True)