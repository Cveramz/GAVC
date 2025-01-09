def handle_titulo_diapositiva(diapositiva) -> str:
    """
    Maneja el contenido de una diapositiva con disposición 'titulo'.
    Las diapositivas con disposición 'titulo' solo contienen un título.
    """
    titulo = diapositiva.get("titulo", "")
    return f"<section>\n<h1>{titulo}</h1>\n</section>\n"
