from flask import jsonify, Blueprint, request
from Controladores.ControladorReportes import ControladorRepostes
from Controladores.CustomExceptions import *

controlador = ControladorRepostes()

reportes = Blueprint('reportes', __name__)


@reportes.route("/detalladoCandidatos", methods=['GET'])
def detalleCandidatos():
    respuesta = controlador.getDetalleCandidatos()
    if respuesta is None:
        return "No se cuenta con resultados en el momento", 200
    return jsonify(respuesta), 200


@reportes.route("/participacionMesas", methods=['GET'])
def participacionMesas():
    respuesta = controlador.getParticipacionMesas()
    if respuesta is None:
        return "No se cuenta con resultados en el momento", 200
    return jsonify(respuesta), 200

@reportes.route("/partidosMesas", methods=['GET'])
def partidosMesas():
    respuesta = controlador.getPartidosDetalleMesa()
    if respuesta is None:
        return "No se cuenta con resultados en el momento", 200
    return jsonify(respuesta), 200

@reportes.route("/partidosParticipacion", methods=['GET'])
def partidosParticipacion():
    respuesta = controlador.getDistribucionPartidos()
    if respuesta is None:
        return "No se cuenta con resultados en el momento", 200
    return jsonify(respuesta), 200
