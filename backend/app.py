import os
from flask import Flask, render_template, request, redirect, url_for, session
from backend.auth import login_user, register_user, logout_user, require_login
from backend.chat import ejecutar_consulta
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "clave-dev")
UPLOAD_FOLDER = 'uploads'

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        if login_user(email, password):
            return redirect(url_for('dashboard'))
        return render_template("login.html", error="Credenciales inválidas")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        register_user(email, password)
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/dashboard", methods=["GET", "POST"])
@require_login
def dashboard():
    respuesta = None
    if request.method == "POST":
        pregunta = request.form["pregunta"]
        respuesta = ejecutar_consulta(pregunta)
    return render_template("dashboard.html", respuesta=respuesta)

if __name__ == "__main__":
    app.run(debug=True)
