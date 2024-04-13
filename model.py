from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuarios(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

class Restaurante(db.Model):
    id_restaurante = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    tipo_comida = db.Column(db.String(50), nullable=False)
    horario_abertura = db.Column(db.Time, nullable=False)
    horario_fechamento = db.Column(db.Time, nullable=False)
