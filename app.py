import os
from flask import Flask, jsonify, url_for, redirect, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# from sqlalchemy.dialects import postgresql
# import psycopg2

app = Flask("__name__")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://znsnbvxrrxdwfb:8d7d8a68a323e888d76cbe01ef24bf39fd3927882d362cb7c0e15b24ef558832@ec2-52-3-200-138.compute-1.amazonaws.com:5432/dahehqr4qgkurb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Modelagem Entidade

class Texto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    text = db.Column(db.String(300))

    def __init__(self, title, text):
        self.title = title
        self.text = text

class TextoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Texto


# Criação de Rotas

@app.route("/")
def index():
    return redirect(url_for("showAllTexts"))


@app.route("/texts", methods=["GET", "DELETE"])
def showAllTexts():
    texts = Texto.query.all()
    texto_schema = TextoSchema(many=True)
    result = texto_schema.dump(texts)
    return render_template("index.html", result=result)


@app.route("/texts/add/", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        data = request.json
        text = Texto(data["title"], data["text"])
        db.session.add(text)
        db.session.commit()
        return jsonify(data)
    return render_template("index.html")


@app.route("/texts/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    text = Texto.query.get(id)
    if request.method == "POST":
        data = request.json
        text.title = data["title"]
        text.text = data["text"]
        db.session.add(text)
        db.session.commit()
        return Response().status_code
    return render_template("index.html")

@app.route("/texts/delete/<int:id>", methods=["GET", "DELETE"])
def delete(id):
    text = Texto.query.get(id)
    db.session.delete(text)
    db.session.commit()
    if Response().status_code == 200:
        return redirect(url_for("showAllTexts"))



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    db.create_all()
    app.run(host='0.0.0.0', port=port)