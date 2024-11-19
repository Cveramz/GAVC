import xml.etree.ElementTree as ET

def crear_presentacion_desde_xml(xml_path):
    # Verificar si el XML es válido
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error: El archivo XML no es válido.\nDetalles del error: {e}")
        return

    # Cargar la plantilla HTML
    with open("templates/plantillaUsach.html", "r", encoding="utf-8") as file:
        plantilla = file.read()

    # Construir el contenido de las diapositivas
    contenido_slides = ""
    for slide in root.findall('Slide'):
        contenido_slide = ""

        for elem in slide:
            text = elem.text if elem.text is not None else ""
            tts_text = elem.attrib.get('tts', '')

            if elem.tag.startswith("Titulo"):
                
                nivel_titulo = elem.tag.replace("Titulo", "")
                if nivel_titulo.isdigit():
                    nivel_titulo = int(nivel_titulo)
                    if 1 <= nivel_titulo <= 6:
                        contenido_slide += f'<h{nivel_titulo} data-tts="{tts_text}">{text}</h{nivel_titulo}>'
                    else:
                        # Si el nivel está fuera del rango 1-6, tratarlo como un `div` genérico
                        contenido_slide += f'<div data-tts="{tts_text}">{text}</div>'
                else:
                    # Si no tiene un nivel válido, tratarlo como un `div` genérico
                    contenido_slide += f'<div data-tts="{tts_text}">{text}</div>'
            elif elem.tag == "Parrafo":
                contenido_slide += f'<p data-tts="{tts_text}">{text}</p>'
            else:
                contenido_slide += f'<div>{text}</div>'

        contenido_slides += f"""
        <section>
            {contenido_slide}
        </section>
        """

    contenido_final = plantilla.replace("{{ content }}", contenido_slides)

    # Guardar el archivo HTML final
    with open("presentacion.html", "w", encoding="utf-8") as f:
        f.write(contenido_final)

# Ruta al archivo XML
xml_path = "xmlexample.xml"
crear_presentacion_desde_xml(xml_path)
