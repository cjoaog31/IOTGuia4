from flask import jsonify, Blueprint, request
from Controladores.ControladorResultadoCandidato import ControladorResultadoCandidato
from Controladores.CustomExceptions import *

controlador = ControladorResultadoCandidato()

resultadocandidato = Blueprint('resultadocandidato', __name__)


@resultadocandidato.route("/resultadoCandidato", methods=['POST'])
def create():
    data = request.get_json()
    try:
        controlador.create(data)
        return "El objeto fue creado correctamente", 201
    except ObjectAlreadyDefined as e:
        return str(e), 404


@resultadocandidato.route("/resultadoCandidato", methods=['GET'])
def listar():
    return jsonify(controlador.list())


@resultadocandidato.route("/resultadoCandidato/<id>", methods=['GET'])
def get(id):
    try:
        resultado = controlador.get(id)
        return jsonify(resultado), 200
    except ObjectNotFound as e:
        return str(e), 404


@resultadocandidato.route("/resultadoCandidato", methods=['PUT'])
def modify():
    data = request.get_json()
    try:
        controlador.modify(data)
        return "Se ha modificado el resultado correctamente", 200
    except ObjectNotFound as e:
        return str(e), 404
    except DuplicateConstrainedValue as e:
        return str(e), 400
    except AttributeError as e:
        return str(e), 400


@resultadocandidato.route("/resultadoCandidato/<id>", methods=['DELETE'])
def delete(id):
    try:
        controlador.delete(id)
        return "Se ha eliminado el resultado correctamente", 200
    except ObjectNotFound as e:
        return str(e), 404
