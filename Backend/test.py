import os
import shutil
import zipfile
import uuid
from fastapi import FastAPI, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
import xml.etree.ElementTree as ET
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMPLATES_DIR = "templates"
RESOURCES_DIR = "."

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

def crear_presentacion_desde_xml(xml_path, output_dir):
    root = cargar_xml(xml_path)
    if root is None:
        return None
    plantilla_path = os.path.join(TEMPLATES_DIR, "plantillaUsach.html")
    plantilla = cargar_plantilla_html(plantilla_path)
    contenido_slides = construir_contenido_diapositivas(root)
    contenido_final = plantilla.replace("{{ content }}", contenido_slides)
    output_html_path = os.path.join(output_dir, "presentacion.html")
    guardar_presentacion_html(contenido_final, output_html_path)
    return output_html_path

async def cleanup_directory(directory: str):
    shutil.rmtree(directory)

@app.post("/generate-presentation/")
async def generate_presentation(file: UploadFile, background_tasks: BackgroundTasks):
    unique_id = str(uuid.uuid4())
    output_dir = os.path.join("output", unique_id)
    os.makedirs(output_dir, exist_ok=True)
    xml_path = os.path.join(output_dir, "input.xml")
    with open(xml_path, "wb") as f:
        f.write(await file.read())
    html_path = crear_presentacion_desde_xml(xml_path, output_dir)
    if html_path is None:
        shutil.rmtree(output_dir)
        return {"error": "Error al procesar el archivo XML."}
    for resource_dir in ["css", "images", "plugin", "dist"]:
        src_path = os.path.join(RESOURCES_DIR, resource_dir)
        dst_path = os.path.join(output_dir, resource_dir)
        if os.path.exists(dst_path):
            shutil.rmtree(dst_path)
        shutil.copytree(src_path, dst_path)
    zip_path = os.path.join(output_dir, "presentation.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path != zip_path:
                    zipf.write(file_path, os.path.relpath(file_path, output_dir))
    if not os.path.exists(zip_path):
        shutil.rmtree(output_dir)
        return {"error": "Error al crear el archivo ZIP."}
    response = FileResponse(zip_path, media_type="application/zip", filename="presentation.zip")
    background_tasks.add_task(cleanup_directory, output_dir)
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
