import inspect
from db import db
from Controladores.CustomExceptions import IncorrectAttribute


class Partido(db.Model):
    __tablename__ = "partido"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True)
    lema = db.Column(db.String(255))
    candidatos = db.relationship('Candidato', backref = 'partido', lazy=True)

    def __init__(self, data, **kwargs):
        self.nombre = data["nombre"]
        self.lema = data["lema"]

    def dict_repr(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "lema": self.lema
        }

    def modify(self, data: dict):
        """
        Modifica los atributos de un partido según los valores recibidos
        :param data: dict - Diccionario con los datos a modificar
        """
        keys = data.keys()
        atributos = self.getAttributes()
        toDoModifications = []
        for key in keys:
            if key not in atributos:
                raise IncorrectAttribute(f"El atributo {key} no se encuentra definido para el partido")
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

    def __repr__(self):
        return f"Nombre: {self.nombre}, Lema: {self.lema}"
