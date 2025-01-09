def handle_individual_diapositiva(diapositiva) -> str:
    """
    Maneja el contenido de una diapositiva con disposición 'individual',
    incluyendo el atributo 'tts' en las etiquetas HTML generadas si está presente.
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
        tts_html = f' tts="{tts_attr}"' if tts_attr else ""  # Incluir 'tts' si existe

        # Mapear la justificación a estilos de CSS
        if justificacion == "izquierda":
            align_style = "align-items: flex-start; text-align: left;"
        elif justificacion == "derecha":
            align_style = "align-items: flex-end; text-align: right;"
        else:  # Por defecto, "centrado"
            align_style = "align-items: center; text-align: center;"
        
        html_content += f"<div style=' height:100% ;flex: 1; display: flex; flex-direction: column; justify-content: center; {align_style}'{tts_html}>"

        # Agregar textos
        for texto in region.findall("texto"):
            texto_content = texto.text if texto.text else ""
            tts_attr = texto.get("tts", "")  # Obtener atributo 'tts' si está presente
            tts_html = f' tts="{tts_attr}"' if tts_attr else ""  # Incluir 'tts' si existe
            html_content += f"""
                <p{tts_html}>{texto_content}</p>
            """

        # Agregar subtítulo
        if region.find("subtitulo") is not None:
            subtitulo = region.find("subtitulo")
            subtitulo_content = subtitulo.text.strip()
            tts_attr = subtitulo.get("tts", "")
            tts_html = f' tts="{tts_attr}"' if tts_attr else ""
            html_content += f"""
            <div>
                <p{tts_html}><strong>{subtitulo_content}</strong></p>
            </div>
            """

        # Agregar código
        if region.find("codigo") is not None:
            codigo = region.find("codigo")
            codigo_content = codigo.text.strip()
            tts_attr = codigo.get("tts", "")
            tts_html = f' tts="{tts_attr}"' if tts_attr else ""
            html_content += f"""
            <pre><code{tts_html} data-trim data-noescape>
            {codigo_content}
            </code></pre>
            """

        # Agregar lista ordenada
        if region.find("listaOrdenada") is not None:
            lista = region.find("listaOrdenada")
            tts_attr = lista.get("tts", "")
            tts_html = f' tts="{tts_attr}"' if tts_attr else ""
            html_content += f"<ol{tts_html}>"
            for item in lista.findall("item"):
                item_content = item.text if item.text else ""
                html_content += f"<li>{item_content}</li>"
            html_content += "</ol>"

        # Agregar lista no ordenada
        if region.find("listaNoOrdenada") is not None:
            lista = region.find("listaNoOrdenada")
            tts_attr = lista.get("tts", "")
            tts_html = f' tts="{tts_attr}"' if tts_attr else ""
            html_content += f"<ul{tts_html}>"
            for item in lista.findall("item"):
                item_content = item.text if item.text else ""
                html_content += f"<li>{item_content}</li>"
            html_content += "</ul>"

        # Agregar tabla con descripción
        if region.find("tabla") is not None:
            tabla = region.find("tabla")
            descripcion = tabla.get("descripcion", "")
            tts_attr = tabla.get("tts", "")
            tts_html = f' tts="{tts_attr}"' if tts_attr else ""
            
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


        # Agregar imagen con descripción
        if region.find("imagen") is not None:
            imagen = region.find("imagen")
            url = imagen.get("url", "")
            descripcion = imagen.get("descripcion", "")
            tts_attr = imagen.get("tts", "")
            tts_html = f' tts="{tts_attr}"' if tts_attr else ""
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


    html_content += f"</div>\n</section>\n"
    return html_content
