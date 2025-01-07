from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
#from validar_xml import validar_xml
import uvicorn
from jinja2 import Environment, FileSystemLoader
import xml.etree.ElementTree as ET
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
import os
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración para Jinja2
env = Environment(loader=FileSystemLoader('templates'))

@app.get("/alive")
def alive():
    """
    Función para verificar que el servidor está corriendo
    """
    return {"status": "Server is running!"}

@app.post("/generate-presentation/")
async def generate_presentation(file: UploadFile):
    """
    Función para generar una presentación HTML a partir de un archivo XML
    """
    if file.content_type not in ["application/xml", "text/xml"]:
        print(f"Tipo de archivo recibido: {file.content_type}")
        raise HTTPException(status_code=400, detail="El archivo debe ser XML.")

    content = await file.read()
    try:
        # Parsear el XML
        tree = ET.ElementTree(ET.fromstring(content))
        root = tree.getroot()

        # Inicializar el contenido HTML
        html_content = ""

        # Buscar las diapositivas y generar el contenido HTML
        for diapositiva in root.findall(".//Diapositiva"):
            disposicion = diapositiva.get("disposicion")
            titulo = diapositiva.get("titulo", "")

            if disposicion == "titulo":
                # Generar HTML para diapositiva con disposición "titulo"
                html_content += f"<section>\n<h1>{titulo}</h1>\n</section>\n"
            elif disposicion == "individual":
                # Generar HTML para diapositiva con disposición "individual"
                # Buscar todas las regiones dentro de la diapositiva
                html_content += f"<section>\n"
                html_content += f"<div style='display: flex; flex-direction: column; height: 100vh;'>"
                
                # Título de la diapositiva
                html_content += f"""
                <div style="height: 10vh; display: flex; justify-content: center; align-items: center; color: white;">
                    <h3>{titulo}</h3>
                </div>
                """
                
                # Recorrer todas las regiones dentro de la diapositiva
                for region in diapositiva.findall(".//region"):
                    region_textos = region.findall("texto")
                    region_codigo = region.find("codigo")
                    
                    html_content += f"<div style='flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center;'>"

                    # Si la región tiene texto(s), agregarlos
                    for texto in region_textos:
                        texto_content = texto.text if texto.text else ""
                        html_content += f"""
                        <div style="display: flex; justify-content: center; align-items: center; margin: 10px 0;">
                            <p>{texto_content}</p>
                        </div>
                        """

                    # Si la región tiene un código, agregarlo
                    if region_codigo is not None and region_codigo.text:
                        codigo_content = region_codigo.text.strip()
                        html_content += f"""
                        <pre><code data-trim data-noescape>
                        {codigo_content}
                        </code></pre>
                        """

                    html_content += f"</div>"  # Cerrar la región

                html_content += f"</div>\n</section>\n"
        
        # Cargar la plantilla HTML
        template = env.get_template("plantilla.html")

        # Renderizar la plantilla con el contenido dinámico
        rendered_html = template.render(content=html_content)

        # Crear un archivo temporal con un nombre único
        os.makedirs("output", exist_ok=True)
        unique_filename = f"output/{uuid.uuid4().hex}.html"
        with open(unique_filename, "w", encoding="utf-8") as f:
            f.write(rendered_html)

        # Retornar el archivo HTML y programar su eliminación después de la respuesta
        def cleanup():
            if os.path.exists(unique_filename):
                os.remove(unique_filename)

        response = FileResponse(
            unique_filename,
            media_type="text/html",
            filename="presentation.html",
            background=BackgroundTask(cleanup)
        )
        return response

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar el XML: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
