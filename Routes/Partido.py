from flask import jsonify, Blueprint, request
from Controladores.ControladorPartido import ControladorPartido
from Controladores.CustomExceptions import *

controlador = ControladorPartido()

partido = Blueprint('partido', __name__)


@partido.route("/partidos", methods=['POST'])
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


@partido.route("/partidos", methods=['GET'])
def listar():
    return jsonify(controlador.list())


@partido.route("/partidos/<id>", methods=['GET'])
def get(id):
    try:
        partido = controlador.get(id)
        return jsonify(partido), 200
    except ObjectNotFound as e:
        return str(e), 404


@partido.route("/partidos", methods=['PUT'])
def modify():
    data = request.get_json()
    try:
        controlador.modify(data)
        return "Se ha modificado el partido correctamente", 200
    except ObjectNotFound as e:
        return str(e), 404
    except DuplicateConstrainedValue as e:
        return str(e), 400
    except AttributeError as e:
        return str(e), 400
    except IncorrectValue as e:
        return str(e), 400
    except IncorrectCreationAttributes as e:
        return str(e), 400


@partido.route("/partidos/<id>", methods=['DELETE'])
def delete(id):
    try:
        controlador.delete(id)
        return "Se ha eliminado el partido correctamente", 200
    except ObjectNotFound as e:
        return str(e), 404