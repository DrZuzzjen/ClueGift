"""
Módulo para gestionar el progreso y estado del juego.
"""
import yaml

def load_clues():
    """
    Carga las pistas desde el archivo YAML.
    
    Returns:
        dict: Datos de las pistas
    """
    with open("clues.yaml", 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def load_progress():
    """
    Carga el progreso desde el archivo YAML.
    
    Returns:
        dict: Datos del progreso
    """
    try:
        with open("progress.yaml", 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        # Si el archivo no existe, devolver valores predeterminados
        return {"completed_questions": [], "current_question": 1, "clues_revealed": 0}

def save_progress(progress_data):
    """
    Guarda el progreso en el archivo YAML.
    
    Args:
        progress_data (dict): Datos del progreso a guardar
    """
    with open("progress.yaml", 'w', encoding='utf-8') as file:
        yaml.dump(progress_data, file)

def reset_progress():
    """
    Reinicia el progreso a valores iniciales.
    
    Returns:
        dict: Datos del progreso reiniciado
    """
    progress_data = {"completed_questions": [], "current_question": 1, "clues_revealed": 0}
    save_progress(progress_data)
    return progress_data

def get_current_question(clues_data, progress_data):
    """
    Obtiene la pregunta actual basada en el progreso.
    
    Args:
        clues_data (dict): Datos de las pistas
        progress_data (dict): Datos del progreso
        
    Returns:
        dict: Pregunta actual o None si no se encuentra
    """
    current_id = progress_data["current_question"]
    for question in clues_data["questions"]:
        if question["id"] == current_id:
            return question
    return None