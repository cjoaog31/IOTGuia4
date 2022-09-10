import inspect

from db import db
from Controladores.CustomExceptions import IncorrectAttribute, IncorrectValue


class Mesa(db.Model):
    __tablename__ = "mesa"

    id = db.Column(db.Integer, primary_key=True)
    numero_mesa = db.Column(db.Integer, unique=True)
    cantidad_inscritos = db.Column(db.Integer, nullable=False)
    resultados = db.relationship('ResultadoCandidato', backref = 'mesa', lazy=True)

    omited_attributes = ['id', 'resultados', 'query', 'registry', 'metadata']

    def __init__(self, data, **kwargs):
        numeroMesa = data["numero_mesa"]
        cantidadInscritos = data["cantidad_inscritos"]

        if numeroMesa <= 0:
            raise IncorrectValue("El numero de mesa no puede ser menor a 1")
        if cantidadInscritos <= 0:
            raise IncorrectValue("El numero de inscritos no puede ser menor a 1")

        self.numero_mesa = numeroMesa
        self.cantidad_inscritos = cantidadInscritos

    def dict_repr(self):
        return {
            "id": self.id,
            "numero_mesa": self.numero_mesa,
            "cantidad_inscritos": self.cantidad_inscritos
        }

    def modify(self, data: dict):
        """
        Modifica los atributos de una mesa según los valores recibidos
        :param data: dict - Diccionario con los datos a modificar
        """
        keys = data.keys()
        atributos = self.getAttributes()
        toDoModifications = []

        if "numero_mesa" in keys:
            numeroMesa = data["numero_mesa"]
            if numeroMesa <= 0:
                raise IncorrectValue("El numero de mesa no puede ser menor a 1")
        if "cantidad_inscritos" in keys():
            cantidadInscritos = data["cantidad_inscritos"]
            if cantidadInscritos <= 0:
                raise IncorrectValue("El numero de inscritos no puede ser menor a 1")

        for key in keys:
            if key not in atributos:
                raise IncorrectAttribute(f"El atributo {key} no se encuentra definido para la mesa")
            currentValue = getattr(self, key)
            newValue = data[key]
            if currentValue != newValue:
                toDoModifications.append((key, newValue))

        for modification in toDoModifications:
            setattr(self, modification[0], modification[1])
        db.session.commit()

    def getAttributes(self):
        """
        Retorna la lista de atributos de la clase y la instancia
        :return: list[(atributo, valor)] - Lista compuesta por los atributos de la clase y la instancia
        """
        resultado = []
        for i in inspect.getmembers(self):
            if not i[0].startswith('_'):
                if not inspect.ismethod(i[1]):
                    resultado.append(i[0])
        return resultado

    @staticmethod
    def __getAttributes__():
        """
        Retorna la lista de atributos de la clase y la instancia
        :return: list[(atributo, valor)] - Lista compuesta por los atributos de la clase y la instancia
        """
        resultado = []
        for i in inspect.getmembers(Mesa):
            if not i[0].startswith('_'):
                if (not callable(i[1])) and i[0] != 'omited_attributes' and i[0] not in Mesa.omited_attributes:
                    resultado.append(i[0])
        return resultado

    def __repr__(self):
        return f"Numero mesa: {self.numero_mesa}, Cantidad de inscritos: {self.cantidad_inscritos}"
