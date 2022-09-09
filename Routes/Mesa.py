from flask import jsonify, Blueprint, request
from Controladores.ControladorMesa import ControladorMesa
from Controladores.CustomExceptions import *

controlador = ControladorMesa()

mesa = Blueprint('mesa', __name__)


@mesa.route("/mesas", methods=['POST'])
def create():
    data = request.get_json()
    try:
        controlador.create(data)
        return "El objeto fue creado correctamente", 201
    except ObjectAlreadyDefined as e:
        return str(e), 404
    except IncorrectCreationAttributes as e:
        return str(e), 400


@mesa.route("/mesas", methods=['GET'])
def listar():
    return jsonify(controlador.list())


@mesa.route("/mesas/<id>", methods=['GET'])
def get(id):
    try:
        mesa = controlador.get(id)
        return jsonify(mesa), 200
    except ObjectNotFound as e:
        return str(e), 404


@mesa.route("/mesas", methods=['PUT'])
def modify():
    data = request.get_json()
    try:
        controlador.modify(data)
        return "Se ha modificado la mesa correctamente", 200
    except ObjectNotFound as e:
        return str(e), 404
    except DuplicateConstrainedValue as e:
        return str(e), 400
    except AttributeError as e:
        return str(e), 400


@mesa.route("/mesas/<id>", methods=['DELETE'])
def delete(id):
    try:
        controlador.delete(id)
        return "Se ha eliminado la mesa correctamente", 200
    except ObjectNotFound as e:
        return str(e), 404