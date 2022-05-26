from flask import Flask, jsonify, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql
import psycopg2

app = Flask("__name__")
app.config["SQLALCHEMY_DATABASE_URI"] = ""
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Modelagem Entidade

class Texto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    text = db.Column(db.String(300))

    def __init__(self, title, text):
        self.title = title
        self.text = text

# Criação de Rotas

@app.route("/")
def index():
    return redirect(url_for("texts"))   

@app.route("/texts", methods=["GET"])
def showAllTexts():
    query = Texto.query.all()
    return jsonify(query)


if __name__ == '__main__':
    app.run()