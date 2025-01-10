def add_data_tts(attribute_value: str, tag: str, content: str) -> str:
    """
    Genera una etiqueta HTML con el atributo data-tts si se proporciona un valor.
    """
    if attribute_value:
        return f'<{tag} data-tts="{attribute_value}">{content}</{tag}>\n'
    else:
        return f'<{tag}>{content}</{tag}>\n'
