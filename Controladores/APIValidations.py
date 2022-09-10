def validateRequiredCreationValues(data: dict, attributes: list):
    keys = data.keys()

    for attribute in attributes:
        if attribute != 'id':
            if attribute not in keys:
                return False;

    for key in keys:
        if key not in attributes:
            return False

    return True


def validatePosibleModificationValues(data: dict, attributes: list):
    keys = data.keys()
    for key in keys:
        if key not in attributes and key != "id":
            return False

    return True
