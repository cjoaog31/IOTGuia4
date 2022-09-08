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