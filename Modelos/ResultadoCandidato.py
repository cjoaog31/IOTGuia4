import inspect
from db import db
from Controladores.CustomExceptions import IncorrectAttribute


class ResultadoCandidato(db.Model):
    __tablename__ = "resultadocandidato"
    __table_args__ = (db.UniqueConstraint('mesa_id', 'candidato_id', name='unique_mesa_candidato'),)

    id = db.Column(db.Integer, primary_key=True)
    mesa_id = db.Column(db.Integer, db.ForeignKey('mesa.id'), nullable=False)
    candidato_id = db.Column(db.Integer, db.ForeignKey('candidato.id'), nullable=False)
    cantidad_votos = db.Column(db.Integer, nullable=False)


    def __init__(self, data, **kwargs):
        self.mesa_id = data["mesa_id"]
        self.candidato_id = data["candidato_id"]
        self.cantidad_votos = data["cantidad_votos"]

    def dict_repr(self):
        return {
            "id": self.id,
            "mesa_id": self.mesa_id,
            "candidato_id": self.candidato_id,
            "cantidad_votos": self.cantidad_votos
        }

    def modify(self, data: dict):
        """
        Modifica los atributos de un resultado según los valores recibidos
        :param data: dict - Diccionario con los datos a modificar
        """
        keys = data.keys()
        atributos = self.getAttributes()
        toDoModifications = []
        for key in keys:
            if key not in atributos:
                raise IncorrectAttribute(f"El atributo {key} no se encuentra definido para los resultados")
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
        return f"Mesa: {self.mesa.id}, Candidato: {self.candidato.nombre} {self.candidato.apellido}, Votos: {self.cantidad_votos}"
