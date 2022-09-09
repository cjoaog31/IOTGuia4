from Modelos.Candidato import Candidato
from Controladores.ControladorPartido import ControladorPartido
from db import db
from Controladores.CustomExceptions import *
from Controladores.APIValidations import *


class ControladorCandidato:
    def __init__(self):
        pass

    def list(self):
        """
        Lista todos los candidatos que se encuentran creados en base de datos
        :return: list: Lista con los candidatos en con su representacion en diccionario
        """
        resultado = Candidato.query.all()

        lista = []
        for i in resultado:
            lista.append(i.dict_repr())
        return lista

    def get(self, id: int):
        """
        Obtiene la representacion en diccionario de un candidato identificado con el id proporcionado
        :param id: id del candidato a buscar en base de datos
        :return: dict - Representacion en diccionario de los datos del candidato
        :raises: ObjectNotFound - En caso de que el objeto no sea encontrado
        """
        resultado = Candidato.query.get(id)
        if resultado is None:
            raise ObjectNotFound("No existe un candidato con el id suministrado")
        return resultado.dict_repr()

    def create(self, data: dict):
        """
        Crea un candidato con la informacion suministrada
        :param data: dict: diccionario con los datos requeridos para crear el candidato en base de datos
        """
        if not validateRequiredCreationValues(data, Candidato.__getAttributes__()):
            raise IncorrectCreationAttributes(
                f"Se suministraron los atributos incorrectos para este endpoint.\n Se esperan los siguientes: {Candidato.__getAttributes__()}")

        if len(ControladorPartido.list()) == 0:
            raise ObjectNotFound("No existen partidos en el sistema")

        if ControladorPartido.get(data["partido_id"]) is None:
            raise ObjectNotFound("El partido enviado no existe")

        busqueda = Candidato.query.filter_by(cedula=data["cedula"]).first()
        if busqueda is not None:
            raise ObjectAlreadyDefined("Ya existe un candidato con la misma cedula en base de datos")

        candidato = Candidato(data)
        db.session.add(candidato)
        db.session.commit()

    def delete(self, id: int):
        """
        Elimina un registro de candidato según su id
        :param id: id del candidato a eliminar
        """
        resultado = Candidato.query.get(id)
        if resultado is None:
            raise ObjectNotFound("No existe un candidato con el id suministrado")
        db.session.delete(resultado)
        db.session.commit()

    def modify(self, data):
        try:
            id = data.pop("id")
            resultado = Candidato.query.get(id)
        except KeyError:
            raise AttributeError("No se ha suministrado el id para la modificacion")
        if resultado is None:
            raise ObjectNotFound("No existe un candidato con el id suministrado")
        if "cedula" in data.keys():
            candidatoConCedula = Candidato.query.filter_by(cedula=data["cedula"]).first()
            if candidatoConCedula is not None:
                raise DuplicateConstrainedValue("Ya existe un candidato con esta cedula en la base de datos, no es posible realizar esta modificacion")
        resultado.modify(data)
