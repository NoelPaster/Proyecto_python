from flask import Flask, render_template, request, redirect

app = Flask(__name__)

posts= [
    {"usuario": "Maria" , "comentario": "comentario1" , "titulo": "titulo1"},
    {"usuario": "Noel" , "comentario": "comentario2" , "titulo": "titulo2"}
]


@app.route('/')

def home():
    return render_template("home.html", nombre="Maria", posts=posts)

@app.route('/hacerca_de')

def hacerca_de():
    return render_template("hacerca_de.html", nombre="Maria")

@app.route('/login', methods= ["GET" , "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", nombre="Maria")
    elif request.method == "POST":
        print(request.form)
        return redirect('\hacerca_de')
    
@app.route('/nuevo_post', methods= ["GET" , "POST"])
def nuevo_post():
    if request.method == "GET":
        return render_template("nuevo_post.html", nombre="Maria")
    elif request.method == "POST":
        print(request.form)
        return "gracias por el nuevo post"

app.run(debug=True)