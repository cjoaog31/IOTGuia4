from app import db
from Modelos import Mesa

#db.create_all()

##crear

mesa1=Mesa.Mesa(466)
mesa2=Mesa.Mesa(256)

db.session.add_all([mesa1,mesa2])
db.session.commit()

'''



#db.create_all()

##crear

estudiante=Estudiante2.Estudiante2("1010221608","Fernando","Cortes")
estudiante2=Estudiante2.Estudiante2("1010221","James","Rodriguez")

db.session.add_all([estudiante,estudiante2])
db.session.commit()


##leer
##muestra todos los registros
resultado = Estudiante2.Estudiante2.query.all()
print("LOS ESTUDIANTES SON: ")
print(resultado)

#Filtrar por nombre
resultado2=Estudiante2.Estudiante2.query.filter_by(nombre="Fernando")
print (resultado2.all())

#Filtrar por id
resultado3=Estudiante2.Estudiante2.query.get(3)
print (resultado3)


#update o actualizacion
resultado4=Estudiante2.Estudiante2.query.get(3)
resultado4.nombre="Jose"
db.session.add(resultado4)
db.session.commit()
print (resultado4)


#eliminar -delete
resultado5=Estudiante2.Estudiante2.query.get(3)
db.session.delete(resultado5)
db.session.commit()

'''