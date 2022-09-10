from Modelos.Partido import Partido
from db import db
from Controladores.CustomExceptions import *
from Controladores.APIValidations import *


class ControladorPartido:
    def __init__(self):
        pass

    def list(self):
        """
        Lista todos los partidos que se encuentran creados en base de datos
        :return: list: Lista con los partidos en con su representacion en diccionario
        """
        resultado = Partido.query.all()

        lista = []
        for i in resultado:
            lista.append(i.dict_repr())
        return lista

    def get(self, id: int):
        """
        Obtiene la representacion en diccionario de un partido identificado con el id proporcionado
        :param id: id del partido a buscar en base de datos
        :return: dict - Representacion en diccionario de los datos del partido
        :raises: ObjectNotFound - En caso de que el objeto no sea encontrado
        """
        resultado = Partido.query.get(id)
        if resultado is None:
            raise ObjectNotFound("No existe un partido con el id suministrado")
        return resultado.dict_repr()

    def create(self, data: dict):
        """
        Crea un partido con la informacion suministrada
        :param data: dict: diccionario con los datos requeridos para crear el partido en base de datos
        """

        if not validateRequiredCreationValues(data, Partido.__getAttributes__()):
            raise IncorrectCreationAttributes(
                f"Se suministraron los atributos incorrectos para este endpoint.\n Se esperan los siguientes: {Partido.__getAttributes__()}")

        busqueda = Partido.query.filter_by(nombre=data["nombre"]).first()
        if busqueda is not None:
            raise ObjectAlreadyDefined("Ya existe un partido con el mismo nombre en base de datos")

        partido = Partido(data)
        db.session.add(partido)
        db.session.commit()

    def delete(self, id: int):
        """
        Elimina un registro de un partido según su id
        :param id: id del partido a eliminar
        """
        resultado = Partido.query.get(id)
        if resultado is None:
            raise ObjectNotFound("No existe un partido con el id suministrado")
        db.session.delete(resultado)
        db.session.commit()

    def modify(self, data):
        # Validacion del data frame contenga solamente llaves permitidas
        if not validatePosibleModificationValues(data, Partido.__getAttributes__()):
            print(Partido.__getAttributes__())
            raise IncorrectCreationAttributes(f"Se suministraron los atributos incorrectos para este endpoint.\nDebe contener solamente un subgrupo de los siguientes: {Partido.__getAttributes__()} aparte del id del objeto")

        try:
            id = data.pop("id")
            resultado = Partido.query.get(id)
        except KeyError:
            raise AttributeError("No se ha suministrado el id para la modificacion")
        if resultado is None:
            raise ObjectNotFound("No existe un partido con el id suministrado")
        if "nombre" in data.keys():
            partidoConNombre = Partido.query.filter_by(nombre=data["nombre"]).first()
            if partidoConNombre is not None:
                raise DuplicateConstrainedValue("Ya existe un partido con este nombre en la base de datos, no es posible realizar esta modificacion")
        resultado.modify(data)