from utils.add_data_tts import add_data_tts

def handle_titulo_diapositiva(diapositiva) -> str:
    """
    Maneja el contenido de una diapositiva con disposición 'titulo'.
    Las diapositivas con disposición 'titulo' solo contienen un título.
    """
    titulo_text = diapositiva.get("titulo", "").strip()
    tts_text = diapositiva.get("tts", "").strip()

    h1_tag = add_data_tts(tts_text, "h1", titulo_text)
    return f"<section>\n{h1_tag}</section>\n"
