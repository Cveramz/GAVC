import xml.etree.ElementTree as ET

def cargar_xml(xml_path):
    try:
        tree = ET.parse(xml_path)
        return tree.getroot()
    except ET.ParseError as e:
        print(f"Error: El archivo XML no es válido.\nDetalles del error: {e}")
        return None

def cargar_plantilla_html(ruta_plantilla):
    with open(ruta_plantilla, "r", encoding="utf-8") as file:
        return file.read()

def generar_contenido_slide(slide):
    contenido_slide = ""
    for elem in slide:
        text = elem.text if elem.text is not None else ""
        tts_text = elem.attrib.get('tts', '')

        if elem.tag.startswith("Titulo"):
            contenido_slide += generar_titulo(elem, text, tts_text)
        elif elem.tag == "Parrafo":
            contenido_slide += f'<p data-tts="{tts_text}">{text}</p>'
        else:
            contenido_slide += f'<div>{text}</div>'
    return contenido_slide

def generar_titulo(elem, text, tts_text):
    nivel_titulo = elem.tag.replace("Titulo", "")
    if nivel_titulo.isdigit():
        nivel_titulo = int(nivel_titulo)
        if 1 <= nivel_titulo <= 6:
            return f'<h{nivel_titulo} data-tts="{tts_text}">{text}</h{nivel_titulo}>'
    # Si no es un nivel válido o no es un número, se trata como un `div` genérico
    return f'<div data-tts="{tts_text}">{text}</div>'

def construir_contenido_diapositivas(root):
    contenido_slides = ""
    for slide in root.findall('Slide'):
        contenido_slide = generar_contenido_slide(slide)
        contenido_slides += f"""
        <section>
            {contenido_slide}
        </section>
        """
    return contenido_slides

def guardar_presentacion_html(contenido, ruta_salida):
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(contenido)

def crear_presentacion_desde_xml(xml_path):
    root = cargar_xml(xml_path)
    if root is None:
        return

    plantilla = cargar_plantilla_html("templates/plantillaUsach.html")
    contenido_slides = construir_contenido_diapositivas(root)
    contenido_final = plantilla.replace("{{ content }}", contenido_slides)
    guardar_presentacion_html(contenido_final, "presentacion.html")

# Ruta al archivo XML
xml_path = "xmlexample.xml"
crear_presentacion_desde_xml(xml_path)
