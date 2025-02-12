def handle_interactivo_alternativas_diapositiva(diapositiva) -> str:
    """
    Procesa una diapositiva con formato interactivo de alternativas, generando
    un bloque de HTML que muestra una pregunta con respuestas y retroalimentación.
    """
    titulo = diapositiva.get("titulo", "")
    html_content = f"<section data-quiz style='height: 100dvh;'>\n"
    
    # Pregunta principal
    pregunta_element = diapositiva.find(".//pregunta")
    if pregunta_element is not None:
        pregunta_text = pregunta_element.text.strip() if pregunta_element.text else ""
        html_content += f"    # {pregunta_text}\n"
    
    # Contenedor de alternativas
    alternativas_element = diapositiva.find(".//alternativas")
    if alternativas_element is not None:
        for alternativa in alternativas_element.findall("alternativa"):
            texto = alternativa.text.strip() if alternativa.text else ""
            correcta = alternativa.get("correcto", "false").lower() == "true"
            checkmark = "[x]" if correcta else "[ ]"
            html_content += f"    - {checkmark} {texto}\n"
    
    # Retroalimentación
    retroalimentacion_element = diapositiva.find(".//retroalimentacion")
    if retroalimentacion_element is not None:
        retro_text = retroalimentacion_element.text.strip() if retroalimentacion_element.text else ""
        html_content += f"    > {retro_text}\n"
    
    html_content += "</section>\n"
    return html_content
