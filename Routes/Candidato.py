from flask import jsonify, Blueprint, request
from Controladores.ControladorCandidato import ControladorCandidato
from Controladores.CustomExceptions import *

controlador = ControladorCandidato()

candidato = Blueprint('candidato', __name__)


@candidato.route("/candidatos", methods=['POST'])
def create():
    data = request.get_json()
    try:
        controlador.create(data)
        return "El objeto fue creado correctamente", 201
    except ObjectAlreadyDefined as e:
        return str(e), 404
    except ObjectNotFound as e:
        return str(e), 404
    except IncorrectCreationAttributes as e:
        return str(e), 400
    except IncorrectValue as e:
        return str(e), 400


@candidato.route("/candidatos", methods=['GET'])
def listar():
    return jsonify(controlador.list())


@candidato.route("/candidatos/<id>", methods=['GET'])
def get(id):
    try:
        candidato = controlador.get(id)
        return jsonify(candidato), 200
    except ObjectNotFound as e:
        return str(e), 404


@candidato.route("/candidatos", methods=['PUT'])
def modify():
    data = request.get_json()
    try:
        controlador.modify(data)
        return "Se ha modificado el candidato correctamente", 200
    except ObjectNotFound as e:
        return str(e), 404
    except DuplicateConstrainedValue as e:
        return str(e), 400
    except AttributeError as e:
        return str(e), 400
    except IncorrectCreationAttributes as e:
        return str(e), 400
    except IncorrectValue as e:
        return str(e), 400


@candidato.route("/candidatos/<id>", methods=['DELETE'])
def delete(id):
    try:
        controlador.delete(id)
        return "Se ha eliminado el candidato correctamente", 200
    except ObjectNotFound as e:
        return str(e), 404