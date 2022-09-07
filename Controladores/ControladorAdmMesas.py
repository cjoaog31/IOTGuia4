from Modelos import Estudiante


class ControladorAdmMesas():
    def __init__(self):
        print("Creando ControladorAdmMesas")

    def index(self):
        print("Listar todas las mesas: ")
        resultado = Mesa.query.all()
        return [resultado]

    def create(self,infoMesa):
        print("Crear una mesa")
        mesa = Mesa(infoMesa)
        return mesa.__dict__
'''
    def show(self,id):
        print("Mostrando un estudiante con id ", id)
        elEstudiante = {
            "_id": id,
            "cedula": "123",
            "nombre": "Juan",
            "apellido": "Perez"
        }
        return elEstudiante

    def update(self,id,infoEstudiante):
        print("Actualizando estudiante con id ", id)
        elEstudiante = Estudiante(infoEstudiante)
        return elEstudiante.__dict__

    def delete(self,id):
        print("Elimiando estudiante con id ", id)
        return {"deleted_count": 1}

'''