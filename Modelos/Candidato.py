import inspect
from app import db
from Controladores.CustomExceptions import IncorrectAttribute


class Candidato(db.Model):
    __tablename__ = "Candidato"

    id = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.Integer, unique=True, nullable=False)
    numero_resolucion = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(30))
    apellido = db.Column(db.String(50))
    partido_id = db.Column(db.Integer, db.ForeignKey('partido.id'), nullable=False)

    def __init__(self, data, **kwargs):
        self.cedula = data["cedula"]
        self.numero_resolucion = data["numero_resolucion"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.partido_id = data["partido_id"]

    def dict_repr(self):
        return {
            "id": self.id,
            "cedula": self.cedula,
            "numero_resolucion": self.numero_resolucion,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "partido": self.partido.nombre
        }

    def modify(self, data: dict):
        """
        Modifica los atributos de un candidato según los valores recibidos
        :param data: dict - Diccionario con los datos a modificar
        """
        keys = data.keys()
        atributos = self.getAttributes()
        toDoModifications = []
        for key in keys:
            if key not in atributos:
                raise IncorrectAttribute(f"El atributo {key} no se encuentra definido para el candidato")
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
        return f"Cedula: {self.cedula}, Nombre: {self.nombre} {self.apellido}, Partido: {self.partido.id}"
