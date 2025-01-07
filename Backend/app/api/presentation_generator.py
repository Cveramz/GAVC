from jinja2 import Environment, FileSystemLoader
import xml.etree.ElementTree as ET
import os
import uuid

env = Environment(loader=FileSystemLoader('templates'))

def generate_presentation_html(xml_content: bytes) -> str:
    """
    Genera el contenido HTML de la presentación a partir del XML proporcionado.
    """
    tree = ET.ElementTree(ET.fromstring(xml_content))
    root = tree.getroot()

    html_content = ""

    for diapositiva in root.findall(".//Diapositiva"):
        disposicion = diapositiva.get("disposicion")
        titulo = diapositiva.get("titulo", "")

        if disposicion == "titulo":
            html_content += f"<section>\n<h1>{titulo}</h1>\n</section>\n"
        elif disposicion == "individual":
            html_content += f"<section>\n"
            html_content += f"<div style='display: flex; flex-direction: column; height: 100vh;'>"
            
            html_content += f"""
            <div style="height: 10vh; display: flex; justify-content: center; align-items: center; color: white;">
                <h3>{titulo}</h3>
            </div>
            """
            
            for region in diapositiva.findall(".//region"):
                region_textos = region.findall("texto")
                region_codigo = region.find("codigo")
                
                html_content += f"<div style='flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center;'>"

                for texto in region_textos:
                    texto_content = texto.text if texto.text else ""
                    html_content += f"""
                    <div style="display: flex; justify-content: center; align-items: center; margin: 10px 0;">
                        <p>{texto_content}</p>
                    </div>
                    """

                if region_codigo is not None and region_codigo.text:
                    codigo_content = region_codigo.text.strip()
                    html_content += f"""
                    <pre><code data-trim data-noescape>
                    {codigo_content}
                    </code></pre>
                    """

                html_content += f"</div>"  # Cerrar la región

            html_content += f"</div>\n</section>\n"

    template = env.get_template("plantilla.html")
    rendered_html = template.render(content=html_content)

    return rendered_html
