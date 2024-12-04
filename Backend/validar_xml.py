import xml.etree.ElementTree as ET

def validar_xml(xml_path):
    """Valida que el XML tenga la estructura especificada."""
    try:
        # Cargar el archivo XML
        with open(xml_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Verificar que comience con la declaración XML
        if not content.strip().startswith('<?xml version ="1.0" encoding="UTF-8"?>'):
            print("Error: La declaración XML debe ser exactamente '<?xml version =\"1.0\" encoding=\"UTF-8\"?>'.")
            return False

        # Verificar que el XML sea bien formado
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Verificar que el nodo raíz sea 'Videoclase'
        if root.tag != 'Videoclase':
            print("Error: El nodo raíz no es 'Videoclase'.")
            return False

        # Verificar que solo contiene los nodos 'Metadatos' y/o 'Contenido'
        hijos_validos = {'Metadatos', 'Contenido'}
        for child in root:
            if child.tag not in hijos_validos:
                print(f"Error: Nodo no permitido '{child.tag}' dentro de 'Videoclase'.")
                return False

            # Validar el contenido de 'Metadatos'
            if child.tag == 'Metadatos':
                if not validar_metadatos(child):
                    return False

            # Validar el contenido de 'Contenido'
            if child.tag == 'Contenido':
                if not validar_contenido(child):
                    return False

        # Validación exitosa
        return True
    except ET.ParseError as e:
        print(f"Error: El archivo XML no es válido.\nDetalles del error: {e}")
        return False
    except Exception as e:
        print(f"Error al leer el archivo XML.\nDetalles del error: {e}")
        return False

def validar_metadatos(metadatos):
    """Valida que 'Metadatos' contenga solo los nodos permitidos y cumpla con las reglas específicas."""
    hijos_validos = {'SoftwareVersion', 'Titulo', 'Autoria', 'Fecha'}
    conteo_autorias = 0

    for child in metadatos:
        if child.tag not in hijos_validos:
            print(f"Error: Nodo no permitido '{child.tag}' dentro de 'Metadatos'.")
            return False

        if child.tag == 'Autoria':
            conteo_autorias += 1

    # Verificar el rango de 'Autoria'
    if conteo_autorias < 1 or conteo_autorias > 3:
        print(f"Error: 'Metadatos' debe contener entre 1 y 3 nodos 'Autoria'. Actualmente hay {conteo_autorias}.")
        return False

    # Validación exitosa
    return True

def validar_contenido(contenido):
    """Valida que 'Contenido' contenga al menos una etiqueta 'Diapositiva'."""
    conteo_diapositivas = 0

    for child in contenido:
        if child.tag == 'Diapositiva':
            conteo_diapositivas += 1
            if not validar_diapositiva(child):
                return False

    # Verificar que haya al menos una 'Diapositiva'
    if conteo_diapositivas < 1:
        print("Error: 'Contenido' debe contener al menos una etiqueta 'Diapositiva'.")
        return False

    # Validación exitosa
    return True

def validar_diapositiva(diapositiva):
    """Valida que 'Diapositiva' cumpla las reglas de contenido."""
    conteo_interactivo = 0
    conteo_region = 0

    for child in diapositiva:
        if child.tag == 'Interactivo':
            conteo_interactivo += 1
        elif child.tag == 'Region':
            conteo_region += 1
            if not validar_region(child):
                return False
        else:
            print(f"Error: Nodo no permitido '{child.tag}' dentro de 'Diapositiva'.")
            return False

    # Regla: Si contiene nodos hijos, debe ser 'Interactivo' o 'Region', pero no ambos
    if conteo_interactivo > 0 and conteo_region > 0:
        print("Error: 'Diapositiva' no puede contener ambos nodos 'Interactivo' y 'Region'.")
        return False

    # Validación exitosa, incluso si está vacía
    return True

def validar_region(region):
    """Valida que 'Region' contenga solo nodos permitidos."""
    hijos_validos = {'Codigo', 'ListaOrdenada', 'ListaNoOrdenada', 'Subtitulo', 'Parrafo', 'Tabla', 'Imagen'}

    for child in region:
        if child.tag not in hijos_validos:
            print(f"Error: Nodo no permitido '{child.tag}' dentro de 'Region'.")
            return False

    # Validación exitosa
    return True
