from Modelos.Registros import Registro
from db import db
from Controladores.CustomExceptions import *
from Controladores.APIValidations import *


class ControladorRegistros:
    def __init__(self):
        pass

    def list(self):
        """
        Lista todos los registros que se encuentran creados en base de datos
        :return: list: Lista con los partidos en con su representacion en diccionario
        """
        resultado = Registro.query.all()

        lista = []
        for i in resultado:
            lista.append(i.dict_repr())
        return lista

    def get(self, id: int):
        """
        Obtiene la representacion en diccionario de un registro identificado con el id proporcionado
        :param id: id del registro a buscar en base de datos
        :return: dict - Representacion en diccionario de los datos del registro
        :raises: ObjectNotFound - En caso de que el objeto no sea encontrado
        """
        resultado = Registro.query.get(id)
        if resultado is None:
            raise ObjectNotFound("No existe un registro con el id suministrado")
        return resultado.dict_repr()

    def create(self, data: dict):
        """
        Crea un registro con la informacion suministrada
        :param data: dict: diccionario con los datos requeridos para crear el registro en base de datos
        """

        if not validateRequiredCreationValues(data, Registro.__getAttributes__()):
            raise IncorrectCreationAttributes(
                f"Se suministraron los atributos incorrectos para este endpoint.\n Se esperan los siguientes: {Registro.__getAttributes__()}")

        registro = Registro(data)
        db.session.add(registro)
        db.session.commit()
