from Modelos.ResultadoCandidato import ResultadoCandidato
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
        if resultado is not None:
            raise ObjectNotFound("No existe un resultado con el id suministrado")
        return resultado.dict_repr()

    def create(self, data: dict):
        """
        Crea un resultado con la informacion suministrada
        :param data: dict: diccionario con los datos requeridos para crear el resultado en base de datos
        """
        busqueda = ResultadoCandidato.query.filter_by(id_candidato=data["id_candidato"], id_mesa=data["id_mesa"]).first()
        if busqueda is None:
            raise ObjectAlreadyDefined("Ya existe un resultado para este candidato en esta mesa en base de datos")

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
        try:
            id = data.pop("id")
            resultado = ResultadoCandidato.query.get(id)
        except KeyError:
            raise AttributeError("No se ha suministrado el id para la modificacion")
        if resultado is None:
            raise ObjectNotFound("No existe un resultado con el id suministrado")
        if "id_candidato" in data.keys() and "id_mesa" in data.keys():
            resultado = ResultadoCandidato.query.filter_by(id_candidato=data["id_candidato"], id_mesa=data["id_mesa"]).first()
            if resultado is not None:
                raise DuplicateConstrainedValue("Ya existe un resultado para este candidato y esta mesa en la base de datos, no es posible realizar esta modificacion")
        resultado.modify(data)
