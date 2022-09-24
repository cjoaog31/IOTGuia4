import inspect
from db import db


class Registro(db.Model):
    __tablename__ = "registro"

    id = db.Column(db.Integer, primary_key=True)
    cantidadActual = db.Column(db.Integer, nullable=False)
    ingresa = db.Column(db.Integer, nullable=False)
    sale = db.Column(db.Integer, nullable=False)
    updateTime = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    omited_attributes = ['query', 'registry', 'metadata', 'id', 'updateTime']

    def __init__(self, data, **kwargs):
        cantidadActual = data["cantidadActual"]
        ingresa = data["ingresa"]
        sale = data["ingresa"]

    def dict_repr(self):
        return {
            "id": self.id,
            "cantidadActual": self.cantidadActual,
            "ingresa": self.ingresa,
            "sale": self.sale,
            "updateTime": self.updateTime
        }

    @staticmethod
    def __getAttributes__():
        """
        Retorna la lista de atributos de la clase y la instancia
        :return: list[(atributo, valor)] - Lista compuesta por los atributos de la clase y la instancia
        """
        resultado = []
        for i in inspect.getmembers(Registro):
            if not i[0].startswith('_'):
                if (not callable(i[1])) and i[0] != 'omited_attributes' and i[0] not in Partido.omited_attributes:
                    resultado.append(i[0])
        return resultado

    def __repr__(self):
        return f"Nombre: {self.nombre}, Lema: {self.lema}"
