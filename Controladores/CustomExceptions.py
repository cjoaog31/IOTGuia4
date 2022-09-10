class ObjectAlreadyDefined(Exception):
    """El objeto a crear ya fue previamente creado en base de datos"""
    pass


class ObjectNotFound(Exception):
    """No se ha encontrado el objeto buscado en base de datos"""
    pass


class IncorrectAttribute(Exception):
    """El atributo suministrado no se encuentra definido en la clase"""
    pass


class DuplicateConstrainedValue(Exception):
    """Existe otro objeto con este valor unico"""
    pass


class MaxResultExceeded(Exception):
    """Se esta excediendo el numero de votos por mesa segun sus inscritos"""
    pass


class IncorrectCreationAttributes(Exception):
    """Los atributos suministrados no son los esperados para esta peticion"""
    pass

class IncorrectValue(Exception):
    """El valos ingresado para uno de los atributos no se encuentra dentro de los parametros aceptados"""
    pass
