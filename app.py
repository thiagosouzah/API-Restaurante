from flask import Flask
from flask_jwt_extended import JWTManager
from model import db
from controller import *

# Configuração do Flask
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Chave secreta para assinar os tokens JWT
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/apirestaurante'  # URL de conexão do banco de dados
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do banco de dados
db.init_app(app)

# Configuração do JWT
jwt = JWTManager(app)

app.route('/register', methods=['POST'])(register)
app.route('/login', methods=['POST'])(login)
app.route('/user/delete', methods=['DELETE'])(delete_Usuario_route)


# Rotas para Restaurante
app.route('/restaurants', methods=['GET'])(get_Restaurantes)
app.route('/restaurant/<int:id_restaurante>', methods=['GET'])(get_Restaurante)
app.route('/restaurant', methods=['POST'])(add_Restaurante_route)
app.route('/restaurant/<int:id_restaurante>', methods=['PUT'])(update_Restaurante_route)
app.route('/restaurant/<int:id_restaurante>', methods=['DELETE'])(delete_Restaurante_route)
app.route('/restaurants/open', methods=['GET'])(get_Restaurantes_Abertos)
app.route('/restaurants/<tipo_comida>', methods=['GET'])(get_Restaurantes_Por_Tipo_Comida)


@app.route('/')
def home():
    return "API is running!"

if __name__ == '__main__':
    app.run(debug=True)
