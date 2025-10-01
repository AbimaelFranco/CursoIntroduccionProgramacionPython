from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "¡Hola, mundo desde Flask!"

@app.route("/saludo")
def saludo():
    return "Bienvenido a la página de saludo."

@app.route("/contacto")
def contacto():
    return "Página de contacto."

if __name__ == "__main__":
    app.run(debug=True)
