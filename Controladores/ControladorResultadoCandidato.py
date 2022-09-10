from Modelos.ResultadoCandidato import ResultadoCandidato
from Controladores.ControladorMesa import ControladorMesa
from Controladores.ControladorCandidato import ControladorCandidato
from Controladores.APIValidations import *
from db import db
from Controladores.CustomExceptions import *


class ControladorResultadoCandidato:
    def __init__(self):
        pass

    def list(self):
        """
        Lista todos los resultados que se encuentran creados en base de datos
        :return: list: Lista con los resultados en con su representacion en diccionario
        """
        resultado = ResultadoCandidato.query.all()

        lista = []
        for i in resultado:
            lista.append(i.dict_repr())
        return lista

    def get(self, id: int):
        """
        Obtiene la representacion en diccionario de un resultado identificado con el id proporcionado
        :param id: id del resultado a buscar en base de datos
        :return: dict - Representacion en diccionario de los datos del resultado
        :raises: ObjectNotFound - En caso de que el objeto no sea encontrado
        """
        resultado = ResultadoCandidato.query.get(id)
        if resultado is None:
            raise ObjectNotFound("No existe un resultado con el id suministrado")
        return resultado.dict_repr()

    def create(self, data: dict):
        """
        Crea un resultado con la informacion suministrada
        :param data: dict: diccionario con los datos requeridos para crear el resultado en base de datos
        """

        if not validateRequiredCreationValues(data, ResultadoCandidato.__getAttributes__()):
            raise IncorrectCreationAttributes(f"Se suministraron los atributos incorrectos para este endpoint.\n Se esperan los siguientes: {ResultadoCandidato.__getAttributes__()}")

        if len(ControladorMesa().list()) == 0:
            raise ObjectNotFound("No existen mesas en el sistema")
        if len(ControladorCandidato().list()) == 0:
            raise ObjectNotFound("No existen candidatos en el sistema")

        busqueda = ResultadoCandidato.query.filter_by(candidato_id=data["candidato_id"], mesa_id=data["mesa_id"]).first()
        if busqueda is not None:
            raise ObjectAlreadyDefined("Ya existe un resultado para este candidato en esta mesa en base de datos")

        id_mesa = data["mesa_id"]
        cantidadASubir = data["cantidad_votos"]
        cantidadActual = self.getActualTotalForTable(id_mesa)
        try:
            mesa = ControladorMesa().getMaxVotantes(id_mesa)
            cantidadMaxima = mesa
            if (cantidadActual + cantidadASubir) > cantidadMaxima:
                raise MaxResultExceeded(
                    "Con la cantidad de votos suministrada se excede el numero de inscritos en la mesa")
        except ObjectNotFound as e:
            pass

        resultadoCandidato = ResultadoCandidato(data)
        db.session.add(resultadoCandidato)
        db.session.commit()

    def delete(self, id: int):
        """
        Elimina un registro de candidato según su id
        :param id: id del candidato a eliminar
        """
        resultado = ResultadoCandidato.query.get(id)
        if resultado is None:
            raise ObjectNotFound("No existe un resultado con el id suministrado")
        db.session.delete(resultado)
        db.session.commit()

    def modify(self, data):

        #Validacion del data frame contenga solamente llaves permitidas
        if not validatePosibleModificationValues(data, ResultadoCandidato.__getAttributes__()):
            raise IncorrectCreationAttributes(f"Se suministraron los atributos incorrectos para este endpoint.\n")

        #Validacion de que contenga el ID el cual es requerido para cualquier modificacion
        try:
            id = data.pop("id")
            resultado = ResultadoCandidato.query.get(id)
        except KeyError:
            raise AttributeError("No se ha suministrado el id para la modificacion")

        #Validacion de la existencia del objeto que se desea modificar
        if resultado is None:
            raise ObjectNotFound("No existe un resultado con el id suministrado")

        #Validacion de que no exista ya una combinacion mesa-candidato en caso de que se desee cambiar alguno de estos valores
        cambiaMesa = True
        cambiaCandidato = False
        if "candidato_id" in data.keys():
            candidato_id = data["candidato_id"]
            if data["candidato_id"] == resultado.candidato_id: cambiaCandidato = False
        else:
            candidato_id = resultado.candidato.id
        if "mesa_id" in data.keys():
            mesa_id = data["mesa_id"]
            if data["mesa_id"] == resultado.mesa_id: cambiaMesa = False
        else:
            mesa_id = resultado.mesa.id
        resultadoBusqueda = ResultadoCandidato.query.filter_by(candidato_id=candidato_id,
                                                               mesa_id=mesa_id).first()
        if resultadoBusqueda is not None and (cambiaMesa or cambiaCandidato):
            raise DuplicateConstrainedValue("Ya existe un resultado para este candidato y esta mesa en la base de datos, no es posible realizar esta modificacion")

        #validacion cantidad de votos no excede capacidad de la mesa destino
        if "cantidad_votos" in data.keys():
            cantidadASubir = data["cantidad_votos"]
        else:
            cantidadASubir = resultado.cantidad_votos
        cantidadActual = self.getActualTotalForTable(mesa_id)
        maximo_votacion = ControladorMesa().getMaxVotantes(mesa_id)
        if cambiaMesa:
            total_votos = cantidadActual + cantidadASubir
        else:
            total_votos = cantidadActual - resultado.cantidad_votos + cantidadASubir
        if total_votos > maximo_votacion:
            raise MaxResultExceeded("Con esta cantidad de votos se excede la cantidad de votantes inscritos en la mesa")

        resultado.modify(data)

    def getActualTotalForTable(self, id: int):
        resultado = ResultadoCandidato.query.filter_by(mesa_id=id)
        cantidad = 0
        for i in resultado:
            cantidad += i.cantidad_votos
        return cantidad
