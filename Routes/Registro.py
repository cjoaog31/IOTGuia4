from flask import jsonify, Blueprint, request
from Controladores.ControladorRegistros import ControladorRegistros
from Controladores.CustomExceptions import *

controlador = ControladorRegistros()

registro = Blueprint('registro', __name__)


@registro.route("/registros", methods=['POST'])
def create():
    data = request.get_json()
    try:
        controlador.create(data)
        return "El objeto fue creado correctamente", 201
    except ObjectAlreadyDefined as e:
        return str(e), 404
    except IncorrectCreationAttributes as e:
        return str(e), 400
    except IncorrectValue as e:
        return str(e), 400


@registro.route("/registros", methods=['GET'])
def listar():
    return jsonify(controlador.list())


@registro.route("/registros/<id>", methods=['GET'])
def get(id):
    try:
        partido = controlador.get(id)
        return jsonify(partido), 200
    except ObjectNotFound as e:
        return str(e), 404

