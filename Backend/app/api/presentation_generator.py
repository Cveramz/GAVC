from jinja2 import Environment, FileSystemLoader
from api.disposiciones.titulo import *
from api.disposiciones.individual import *
from api.disposiciones.duo import *
from api.disposiciones.duo_horizontal import *
from api.disposiciones.cuarteto import *
from api.disposiciones.interactivo_alternativas import *
import xml.etree.ElementTree as ET

env = Environment(loader=FileSystemLoader('templates'))


def generate_presentation_html(xml_content: bytes) -> str:
    """
    Genera el contenido HTML de la presentación a partir del XML proporcionado.
    """
    tree = ET.ElementTree(ET.fromstring(xml_content))
    root = tree.getroot()

    html_content = ""

    for diapositiva in root.findall(".//Diapositiva"):
        disposicion = diapositiva.get("disposicion").lower()

        if disposicion == "titulo":
            html_content += handle_titulo_diapositiva(diapositiva)
        elif disposicion == "individual":
            html_content += handle_individual_diapositiva(diapositiva)
        elif disposicion in ["duo", "duo-vertical"]:
            html_content += handle_duo_diapositiva(diapositiva)
        elif disposicion == "duo-horizontal":
            html_content += handle_duo_horizontal_diapositiva(diapositiva)
        elif disposicion == "cuarteto":
            html_content += handle_cuarteto_diapositiva(diapositiva)
        elif disposicion == "interactivo-alternativas":
            html_content += handle_interactivo_alternativas_diapositiva(diapositiva)

    template = env.get_template("plantilla.html")
    rendered_html = template.render(content=html_content)

    return rendered_html
