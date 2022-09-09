from Modelos.Mesa import Mesa
from db import db
from Controladores.CustomExceptions import *


class ControladorMesa:
    def __init__(self):
        pass

    def list(self):
        """
        Lista todos las mesas que se encuentran creadas en base de datos
        :return: list: Lista con las mesas en con su representacion en diccionario
        """
        resultado = Mesa.query.all()

        lista = []
        for i in resultado:
            lista.append(i.dict_repr())
        return lista

    def get(self, id: int):
        """
        Obtiene la representacion en diccionario de una mesa identificada con el id proporcionado
        :param id: id de la mesa a buscar en base de datos
        :return: dict - Representacion en diccionario de los datos de la mesa
        :raises: ObjectNotFound - En caso de que el objeto no sea encontrado
        """
        resultado = Mesa.query.get(id)
        if resultado is None:
            raise ObjectNotFound("No existe una mesa con el id suministrado")
        return resultado.dict_repr()

    def create(self, data: dict):
        """
        Crea una mesa con la informacion suministrada
        :param data: dict: diccionario con los datos requeridos para crear la mesa en base de datos
        """
        busqueda = Mesa.query.filter_by(numero_mesa=data["numero_mesa"]).first()
        if busqueda is not None:
            raise ObjectAlreadyDefined("Ya existe una mesa con el mismo numero en base de datos")

        mesa = Mesa(data)
        db.session.add(mesa)
        db.session.commit()

    def delete(self, id: int):
        """
        Elimina un registro de una mesa según su id
        :param id: id de la mesa a eliminar
        """
        resultado = Mesa.query.get(id)
        if resultado is None:
            raise ObjectNotFound("No existe una mesa con el id suministrado")
        db.session.delete(resultado)
        db.session.commit()

    def modify(self, data):
        try:
            id = data.pop("id")
            resultado = Mesa.query.get(id)
        except KeyError:
            raise AttributeError("No se ha suministrado el id para la modificacion")
        if resultado is None:
            raise ObjectNotFound("No existe una mesa con el id suministrado")
        if "numero_mesa" in data.keys():
            mesaConNumero = Mesa.query.filter_by(numero_mesa=data["numero_mesa"]).first()
            if mesaConNumero is not None:
                raise DuplicateConstrainedValue("Ya existe una mesa con este numero de mesa en la base de datos, no es posible realizar esta modificacion")
        resultado.modify(data)
