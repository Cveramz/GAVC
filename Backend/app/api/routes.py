# app/api/routes.py
from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
import os
import uuid

#from app.utils.xml_validator import validar_xml
from api.presentation_generator import generate_presentation_html

router = APIRouter()

@router.post("/generate-presentation/")
async def generate_presentation(file: UploadFile):
    """
    Endpoint para generar una presentación HTML a partir de un archivo XML
    """
    if file.content_type not in ["application/xml", "text/xml"]:
        print(f"Tipo de archivo recibido: {file.content_type}")
        raise HTTPException(status_code=400, detail="El archivo debe ser XML.")
    
    content = await file.read()
    try:
        # Validar XML
        #validar_xml(content)
        
        # Generar contenido HTML
        try:
            html_content = generate_presentation_html(content)
        except Exception as e:
            print(f"Error al cargar la funcion de generacion de HTML: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Error al cargar la funcion de generacion de HTML: {str(e)}")
        
        
        
        # Crear un archivo temporal con un nombre único
        os.makedirs("output", exist_ok=True)
        unique_filename = f"output/{uuid.uuid4().hex}.html"
        with open(unique_filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        
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
