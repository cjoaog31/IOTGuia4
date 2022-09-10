import inspect
from db import db
from Controladores.CustomExceptions import IncorrectAttribute, IncorrectValue


class Candidato(db.Model):
    __tablename__ = "candidato"

    id = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.Integer, unique=True, nullable=False)
    numero_resolucion = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(30))
    apellido = db.Column(db.String(50))
    partido_id = db.Column(db.Integer, db.ForeignKey('partido.id'), nullable=False)
    resultados = db.relationship('ResultadoCandidato', backref='candidato', lazy=True)

    omited_attributes = ['resultados', 'query', 'registry', 'metadata', 'id', 'partido']

    def __init__(self, data, **kwargs):
        cc = data["cedula"]
        resolucion = data["numero_resolucion"]
        name = data["nombre"]
        lastName = data["apellido"]

        if cc <= 0:
            raise IncorrectValue("La cedula no puede ser un numero negativo o 0")
        if type(resolucion) is str:
            raise IncorrectValue("La resolucion debe ser un numero")
        if resolucion <= 0:
            raise IncorrectValue("La resolucion no puede ser un numero negativo o 0")
        if len(name) > 30 or name == "":
            raise IncorrectValue("El nombre no puede contener más de 30 caracteres o ser vacio")
        if len(name) > 50 or name == "":
            raise IncorrectValue("El apellido no puede contener más de 50 caracteres o ser vacio")

        self.cedula = cc
        self.numero_resolucion = resolucion
        self.nombre = name
        self.apellido = lastName
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

        if "cedula" in keys:
            cc = data["cedula"]
            if cc <= 0:
                raise IncorrectValue("La cedula no puede ser un numero negativo o 0")
        if "numero_resolucion" in keys:
            resolucion = data["numero_resolucion"]
            if type(resolucion) is str:
                raise IncorrectValue("La resolucion debe ser un numero")
        if "nombre" in keys:
            name = data["nombre"]
            if len(name) > 30 or name == "":
                raise IncorrectValue("El nombre no puede contener más de 30 caracteres o ser vacio")
        if "apellido" in keys:
            lastName = data["apellido"]
            if len(name) > 50 or name == "":
                raise IncorrectValue("El apellido no puede contener más de 50 caracteres o ser vacio")

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

    @staticmethod
    def __getAttributes__():
        """
        Retorna la lista de atributos de la clase y la instancia
        :return: list[(atributo, valor)] - Lista compuesta por los atributos de la clase y la instancia
        """
        resultado = []
        for i in inspect.getmembers(Candidato):
            if not i[0].startswith('_'):
                if (not callable(i[1])) and i[0] != 'omited_attributes' and i[0] not in Candidato.omited_attributes:
                    resultado.append(i[0])
        return resultado

    def __repr__(self):
        return f"Cedula: {self.cedula}, Nombre: {self.nombre} {self.apellido}, Partido: {self.partido.id}"
