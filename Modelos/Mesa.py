import inspect
from db import db
from Controladores.CustomExceptions import IncorrectAttribute


class Mesa(db.Model):
    __tablename__ = "mesa"

    id = db.Column(db.Integer, primary_key=True)
    numero_mesa = db.Column(db.String(50), unique=True)
    cantidad_inscritos = db.Column(db.Integer, nullable=False)
    resultados = db.relationship('ResultadoCandidato', backref = 'mesa', lazy=True)

    def __init__(self, data, **kwargs):
        self.numero_mesa = data["numero_mesa"]
        self.cantidad_inscritos = data["cantidad_inscritos"]

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

    def __repr__(self):
        return f"Numero mesa: {self.numero_mesa}, Cantidad de inscritos: {self.cantidad_inscritos}"
