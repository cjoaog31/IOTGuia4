from app import db


class Mesa(db.Model):
    __tablename__ = "Mesa"

    id = db.Column(db.Integer,primary_key=True)
    cant_inscritos = db.Column(db.Integer())

    def __init__(self,cant_inscritos):
        self.cant_inscritos = cant_inscritos

    def __repr__(self):
        return f"Mesa: {self.id}, Cantidad de inscritos : {self.cant_inscritos}"