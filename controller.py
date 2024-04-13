from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from model import db, Usuarios, Restaurante
from service import register_Usuario, get_Usuario_by_nome, delete_Usuario, get_all_Restaurantes, get_Restaurante_by_id, add_Restaurante, update_Restaurante, delete_Restaurante
from datetime import datetime
import bcrypt

def get_Restaurantes_Abertos():
    current_time = datetime.now().time()
    Restaurantes = get_all_Restaurantes()
    output = []
    for Restaurante in Restaurantes:
        if Restaurante.horario_abertura <= current_time <= Restaurante.horario_fechamento:
            Restaurante_data = {
                'id': Restaurante.id_restaurante,
                'nome': Restaurante.nome,
                'tipo_comida': Restaurante.tipo_comida,
                'horario_abertura': Restaurante.horario_abertura.strftime('%H:%M'),
                'horario_fechamento': Restaurante.horario_fechamento.strftime('%H:%M')
            }
            output.append(Restaurante_data)
    return jsonify({'Restaurantes_Abertos': output}), 200

def register():
    data = request.get_json()
    nome = data.get('nome')
    senha = data.get('senha')
    if nome and senha:
        if get_Usuario_by_nome(nome):
            return jsonify({'message': 'Usuarios already exists'}), 400
        Usuarios = register_Usuario(nome, senha)
        access_token = create_access_token(identity=Usuarios.id_usuario)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'nome and senha are required'}), 400


def login():
    data = request.get_json()
    nome = data.get('nome')
    senha = data.get('senha')
    usuario = get_Usuario_by_nome(nome)
    if usuario and senha == usuario.senha:
        access_token = create_access_token(identity=usuario.id_usuario)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid user name or password'}), 401



@jwt_required()
def delete_Usuario_route():
    current_Usuario = get_jwt_identity()
    if delete_Usuario(current_Usuario):
        return jsonify({'message': 'Usuario deleted successfully'}), 200
    else:
        return jsonify({'message': 'Usuario not found'}), 404

def get_Restaurantes():
    Restaurantes = get_all_Restaurantes()
    output = []
    for Restaurante in Restaurantes:
        Restaurante_data = {
            'id': Restaurante.id_restaurante,
            'nome': Restaurante.nome,
            'tipo_comida': Restaurante.tipo_comida,
            'horario_abertura': Restaurante.horario_abertura.strftime('%H:%M'),
            'horario_fechamento': Restaurante.horario_fechamento.strftime('%H:%M')
        }
        output.append(Restaurante_data)
    return jsonify({'Restaurantes': output}), 200

def get_Restaurante(id_restaurante):
    Restaurante = get_Restaurante_by_id(id_restaurante)
    if Restaurante:
        Restaurante_data = {
            'id': Restaurante.id_restaurante,
            'nome': Restaurante.nome,
            'tipo_comida': Restaurante.tipo_comida,
            'horario_abertura': Restaurante.horario_abertura.strftime('%H:%M'),
            'horario_fechamento': Restaurante.horario_fechamento.strftime('%H:%M')
        }
        return jsonify(Restaurante_data), 200
    else:
        return jsonify({'message': 'Restaurante not found'}), 404

@jwt_required()
def add_Restaurante_route():
    data = request.get_json()
    nome = data.get('nome')
    tipo_comida = data.get('tipo_comida')
    horario_abertura = datetime.strptime(data.get('horario_abertura'), '%H:%M').time()
    horario_fechamento = datetime.strptime(data.get('horario_fechamento'), '%H:%M').time()
    if nome and tipo_comida and horario_abertura and horario_fechamento:
        add_Restaurante(nome, tipo_comida, horario_abertura, horario_fechamento)
        return jsonify({'message': 'Restaurante added successfully'}), 201
    else:
        return jsonify({'message': 'nome, cuisine type, opening time and closing time are required'}), 400

@jwt_required()
def update_Restaurante_route(id_restaurante):
    data = request.get_json()
    nome = data.get('nome')
    tipo_comida = data.get('tipo_comida')
    horario_abertura = datetime.strptime(data.get('horario_abertura'), '%H:%M').time()
    horario_fechamento = datetime.strptime(data.get('horario_fechamento'), '%H:%M').time()
    if nome and tipo_comida and horario_abertura and horario_fechamento:
        if update_Restaurante(id_restaurante, nome, tipo_comida, horario_abertura, horario_fechamento):
            return jsonify({'message': 'Restaurante updated successfully'}), 200
        else:
            return jsonify({'message': 'Restaurante not found'}), 404
    else:
        return jsonify({'message': 'nome, cuisine type, opening time and closing time are required'}), 400


@jwt_required()
def delete_Restaurante_route(id_restaurante):
    if delete_Restaurante(id_restaurante):
        return jsonify({'message': 'Restaurante deleted successfully'}), 200
    else:
        return jsonify({'message': 'Restaurante not found'}), 404


def get_Restaurantes_Por_Tipo_Comida(tipo_comida):
    restaurantes = Restaurante.query.filter_by(tipo_comida=tipo_comida).all()
    if restaurantes:
        output = []
        for restaurante in restaurantes:
            restaurante_data = {
                'id': restaurante.id_restaurante,
                'nome': restaurante.nome,
                'tipo_comida': restaurante.tipo_comida,
                'horario_abertura': restaurante.horario_abertura.strftime('%H:%M'),
                'horario_fechamento': restaurante.horario_fechamento.strftime('%H:%M')
            }
            output.append(restaurante_data)
        return output
    else:
        return None