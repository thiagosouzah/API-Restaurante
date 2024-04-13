from model import db, Usuarios, Restaurante
from flask_bcrypt import Bcrypt
import bcrypt

bcrypt = Bcrypt()

# def register_Usuario(nome, senha):
#     hashed_senha = bcrypt.generate_senha_hash(senha).decode('utf-8')
#     new_Usuario = Usuarios(nome=nome, senha=hashed_senha)
#     db.session.add(new_Usuario)
#     db.session.commit()
#     return new_Usuario

def register_Usuario(nome, senha):
    hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    new_Usuario = Usuarios(nome=nome, senha=hashed_senha)
    db.session.add(new_Usuario)
    db.session.commit()
    return new_Usuario

def get_Usuario_by_nome(nome):
    return Usuarios.query.filter_by(nome=nome).first()

def delete_Usuario(Usuario_id):
    usuario = Usuarios.query.get(Usuario_id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return True
    return False

def get_all_Restaurantes():
    return Restaurante.query.all()

def get_Restaurante_by_id(id_restaurante):
    return Restaurante.query.get(id_restaurante)

def add_Restaurante(nome, tipo_comida, horario_abertura, horario_fechamento):
    new_Restaurante = Restaurante(
        nome=nome,
        tipo_comida=tipo_comida,
        horario_abertura=horario_abertura,
        horario_fechamento=horario_fechamento
    )
    db.session.add(new_Restaurante)
    db.session.commit()
    return new_Restaurante

def update_Restaurante(id_restaurante, nome, tipo_comida, horario_abertura, horario_fechamento):
    restaurante = Restaurante.query.get(id_restaurante)
    if restaurante:
        restaurante.nome = nome
        restaurante.tipo_comida = tipo_comida
        restaurante.horario_abertura = horario_abertura
        restaurante.horario_fechamento = horario_fechamento
        db.session.commit()
        return True
    return False


def delete_Restaurante(restaurante_id):
    restaurante = Restaurante.query.get(restaurante_id)
    if restaurante:
        db.session.delete(restaurante)
        db.session.commit()
        return True
    return False
