def handle_individual_diapositiva(diapositiva) -> str:
    """
    Maneja el contenido de una diapositiva con disposición 'individual',
    incluyendo el atributo 'data-tts' en las etiquetas HTML generadas si está presente.
    Preserva el orden de los elementos según el XML.
    """
    titulo = diapositiva.get("titulo", "")
    html_content = f"<section style='height: 100dvh;'>\n"
    html_content += f"<div style='display: flex; flex-direction: column; height: 100%;'>"
    
    # Título de la diapositiva
    html_content += f"""
    <div style="height: 10%; display: flex; justify-content: center; align-items: center; color: white;">
        <h3>{titulo}</h3>
    </div>
    """
    
    # Manejar regiones dentro de la diapositiva
    for region in diapositiva.findall(".//region"):
        justificacion = region.get("justificacion", "centrado")  # Obtener justificación o predeterminar "centrado"
        tts_attr = region.get("tts", "")  # Obtener atributo 'tts' si está presente
        tts_html = f' data-tts="{tts_attr}"' if tts_attr else ""  # Incluir 'data-tts' si existe

        # Mapear la justificación a estilos de CSS
        if justificacion == "izquierda":
            align_style = "align-items: flex-start; text-align: left;"
        elif justificacion == "derecha":
            align_style = "align-items: flex-end; text-align: right;"
        else:  # Por defecto, "centrado"
            align_style = "align-items: center; text-align: center;"
        
        html_content += f"<div style='height:100%; flex: 1; display: flex; flex-direction: column; justify-content: center; {align_style}'{tts_html}>"

        # Iterar sobre los elementos hijos de la región en el orden del XML
        for element in region:
            if element.tag == "subtitulo":
                subtitulo_content = element.text.strip() if element.text else ""
                tts_attr = element.get("tts", "")
                tts_html = f' data-tts="{tts_attr}"' if tts_attr else ""
                html_content += f"""
                <div>
                    <p{tts_html}><strong>{subtitulo_content}</strong></p>
                </div>
                """
            
            elif element.tag == "texto":
                texto_content = element.text.strip() if element.text else ""
                tts_attr = element.get("tts", "")
                tts_html = f' data-tts="{tts_attr}"' if tts_attr else ""
                html_content += f"""
                    <p{tts_html}>{texto_content}</p>
                """
            
            elif element.tag == "codigo":
                codigo_content = element.text.strip() if element.text else ""
                tts_attr = element.get("tts", "")
                tts_html = f' data-tts="{tts_attr}"' if tts_attr else ""
                html_content += f"""
                <pre><code{tts_html} data-trim data-noescape>
                {codigo_content}
                </code></pre>
                """
            
            elif element.tag == "listaOrdenada":
                tts_attr = element.get("tts", "")
                tts_html = f' data-tts="{tts_attr}"' if tts_attr else ""
                html_content += f"<ol{tts_html}>"
                for item in element.findall("item"):
                    item_content = item.text.strip() if item.text else ""
                    html_content += f"<li>{item_content}</li>"
                html_content += "</ol>"
            
            elif element.tag == "listaNoOrdenada":
                tts_attr = element.get("tts", "")
                tts_html = f' data-tts="{tts_attr}"' if tts_attr else ""
                html_content += f"<ul{tts_html}>"
                for item in element.findall("item"):
                    item_content = item.text.strip() if item.text else ""
                    html_content += f"<li>{item_content}</li>"
                html_content += "</ul>"
            
            elif element.tag == "tabla":
                tabla = element
                descripcion = tabla.get("descripcion", "")
                tts_attr = tabla.get("tts", "")
                tts_html = f' data-tts="{tts_attr}"' if tts_attr else ""
                
                # Iniciar el contenedor de la tabla y la descripción
                html_content += f"""
                <div style="width: 100%; overflow-x: auto;"{tts_html}>
                    <table border='1' style='border-collapse: collapse; width: 100%; min-width: 300px;'>
                """
                
                # Agregar filas y celdas de la tabla
                for fila in tabla.findall("fila"):
                    html_content += "<tr>"
                    for celda in fila.findall("celda"):
                        celda_content = celda.text.strip() if celda.text else ""
                        html_content += f"<td style='padding: 5px; text-align: center; font-size: 0.9em;'>{celda_content}</td>"
                    html_content += "</tr>"
                
                # Cerrar la tabla
                html_content += "</table>"
                
                # Agregar la descripción si existe
                if descripcion:
                    html_content += f"""
                    <div style="text-align: center; font-style: italic; font-size: 0.9em;">
                        <p>{descripcion}</p>
                    </div>
                    """
                
                # Cerrar el contenedor
                html_content += "</div>"
            
            elif element.tag == "imagen":
                imagen = element
                url = imagen.get("url", "")
                descripcion = imagen.get("descripcion", "")
                tts_attr = imagen.get("tts", "")
                tts_html = f' data-tts="{tts_attr}"' if tts_attr else ""
                if url:
                    html_content += f"""
                    <div style="width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center;"{tts_html}>
                        <img src="{url}" alt="{descripcion}" style="max-width: 100%; max-height: 70%; height: auto; object-fit: contain;">
                    """
                    if descripcion:
                        html_content += f"""
                        <div style="text-align: center; font-style: italic; font-size: 0.9em;">
                            <p>{descripcion}</p>
                        </div>
                        """
                    html_content += "</div>"
            
            # Puedes agregar más condiciones aquí si tienes otros tipos de elementos

        html_content += "</div>"  # Cerrar la región

    html_content += f"</div>\n</section>\n"
    return html_content
