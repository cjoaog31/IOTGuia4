from Modelos.ResultadoCandidato import ResultadoCandidato
from Modelos.Candidato import Candidato
from Modelos.Mesa import Mesa
from Modelos.Partido import Partido
from sqlalchemy import func
from sqlalchemy.orm import Session
from Controladores.APIValidations import *
from db import db
from Controladores.CustomExceptions import *

class ControladorRepostes:

    def __init__(self):
        pass

    def __getDetalleCandidato__(self, candidato: Candidato):
        listaResultados = candidato.resultados
        respuesta = {}
        respuesta["id"] = candidato.id
        respuesta["nombre_completo"] = candidato.nombre + " " + candidato.apellido
        respuesta["partido"] = candidato.partido.nombre
        listaResultadosDiccionarios = []
        cantidad_votos = 0
        for resultado in listaResultados:
            diccionario, votos = self.__getDetalleMesaCandidato__(resultado)
            cantidad_votos += votos
            listaResultadosDiccionarios.append((diccionario, votos))
        resultadosMesasOrg = sorted(listaResultadosDiccionarios, key=lambda x: x[1])
        resultadoSinTupla = self.__removerTuplas__(resultadosMesasOrg)
        resultadoSinTupla.reverse()
        respuesta["detalle_mesas"] = resultadoSinTupla
        respuesta["total_votos"] = cantidad_votos
        return respuesta, cantidad_votos

    def __getDetalleMesaCandidato__(self, resultado: ResultadoCandidato):
        resultadoDiccionario = {}
        mesa = resultado.mesa
        resultadoDiccionario["numero_mesa"] = mesa.numero_mesa
        votos = resultado.cantidad_votos
        resultadoDiccionario["cantidad_votos"] = votos
        return resultadoDiccionario, votos

    def __removerTuplas__(self, lista: list):
        resultado = []
        for i in lista:
            resultado.append(i[0])
        return resultado

    def __getDetalleMesa__(self, mesa: Mesa):
        resultado = {}
        resultado["id"] = mesa.id
        total_votos = 0
        listaResultados = mesa.resultados
        for res in listaResultados:
            votos = res.cantidad_votos
            total_votos += votos
        resultado["total_votos"] = total_votos
        return resultado, total_votos

    def getDetalleCandidatos(self):
        listaCandidatos = Candidato.query.all()
        resultado = []
        listaAOrganizar = []
        for candidato in listaCandidatos:
            detalleCandidato, votos = self.__getDetalleCandidato__(candidato)
            listaAOrganizar.append((detalleCandidato, votos))
        listaOrganizada = sorted(listaAOrganizar, key=lambda x: x[1])
        resultado = self.__removerTuplas__(listaOrganizada)
        resultado.reverse()
        print(resultado)
        return resultado

    def getParticipacionMesas(self):
        listaMesas = Mesa.query.all()
        resultado = []
        for mesa in listaMesas:
            resultado.append(self.__getDetalleMesa__(mesa))
        listaOrganizada = sorted(resultado, key=lambda x: x[1])
        return listaOrganizada

    def getPartidosDetalleMesa(self):

        queryPartidos = db.session.query((Partido.nombre).label("partido"),
                                         func.sum(ResultadoCandidato.cantidad_votos).label('total_votos'),
                                         ).select_from(Partido).join(Candidato).join(ResultadoCandidato).join(
            Mesa).group_by(Partido.nombre).order_by(func.sum(ResultadoCandidato.cantidad_votos).desc())
        diccionarioInicial = {}
        for row in queryPartidos:
            diccionarioInterno = {}
            diccionarioInterno["partido"] = row.partido
            diccionarioInterno["total_votos"] = row.total_votos
            diccionarioInterno["detalle_mesas"] = []
            diccionarioInicial[row.partido] = diccionarioInterno

        queryMesas = db.session.query((Partido.nombre).label("partido"),
                                 (Mesa.numero_mesa).label("numero_mesa"),
                            func.sum(ResultadoCandidato.cantidad_votos).label('total_votos'),
                               ).select_from(Partido).join(Candidato).join(ResultadoCandidato).join(Mesa).group_by(
            Partido.nombre, Mesa.numero_mesa).order_by(func.sum(ResultadoCandidato.cantidad_votos).desc())
        for row in queryMesas:
            diccionarioInterno = {}
            diccionarioInterno["numero_mesa"] = row.numero_mesa
            diccionarioInterno["votos_mesa"] = row.total_votos
            diccionarioInicial[row.partido].get("detalle_mesas").append(diccionarioInterno)

        resultado = []
        for key, dato in diccionarioInicial.items():
            resultado.append(dato)

        return resultado

    def getDistribucionPartidos(self):
        subQuery = db.session.query(
            (Candidato.nombre).label('nombre_candidato'), func.sum(ResultadoCandidato.cantidad_votos).label('total_votos'),
            (Partido.nombre).label('partido')).select_from(Partido).join(Candidato).join(ResultadoCandidato).group_by(
            Candidato.nombre, Partido.nombre).order_by(func.sum(ResultadoCandidato.cantidad_votos)).limit(15).subquery()
        query = db.session.query((subQuery.c.partido).label('partido'), func.sum(subQuery.c.total_votos).label("total_votos")).\
            select_from(subQuery).group_by(subQuery.c.partido, subQuery.c.total_votos).order_by(func.sum(subQuery.c.total_votos).desc())

        listaResultado = []
        total_votos = 0
        for row in query:
            diccionarioInterno = {}
            diccionarioInterno['partido'] = row.partido
            diccionarioInterno['total_votos'] = row.total_votos
            total_votos += row.total_votos
            listaResultado.append(diccionarioInterno)

        for partido in listaResultado:
            partido['porcentaje'] = partido.get('total_votos') / total_votos

        return listaResultado

