"""
Módulo para los agentes de IA y funciones relacionadas con LLM.
"""
import streamlit as st
from openai import AzureOpenAI
from style import loading_animation_html

def initialize_client(api_key, api_version, endpoint):
    """Inicializar el cliente de OpenAI para Azure."""
    return AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=endpoint
    )

def answer_grader(client, deployment_name, user_answer, correct_answer, question):
    """
    Agente AnswerGrader para evaluar las respuestas.
    
    Args:
        client: Cliente de AzureOpenAI
        deployment_name: Nombre del modelo desplegado
        user_answer: Respuesta del usuario
        correct_answer: Respuesta correcta
        question: Pregunta original
        
    Returns:
        tuple: (is_correct, full_result)
    """
    # Preparar el prompt
    prompt = f"""
    Sistema: Sos un evaluador de respuestas para un juego de acertijos para una señora argentina de 70 años llamada Claude. 
    Tu trabajo es determinar si la respuesta que dio es correcta o está muy cerca de la respuesta correcta.
    Sé muy generoso en tu evaluación, aceptando respuestas que capturen la esencia correcta.
    
    La pregunta era: "{question}"
    La respuesta correcta es: "{correct_answer}"
    La respuesta del usuario es: "{user_answer}"
    
    Responde SOLAMENTE con "CORRECTO" o "INCORRECTO" seguido de un breve comentario amigable.
    Si es CORRECTO, felicitala con calidez en un tono argentino, como si fueras su amigo/a.
    Si es INCORRECTO, dale un pequeño consejo para ayudarla, sin revelar la respuesta.
    """

    # Llamada al modelo con streaming
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=150,
        stream=True
    )
    
    # Mostrar animación de carga
    result_placeholder = st.empty()
    result_placeholder.markdown(loading_animation_html(), unsafe_allow_html=True)
    
    # Procesar respuesta streaming
    result = []
    
    for chunk in response:
        if chunk.choices:
            content = chunk.choices[0].delta.content
            if content:
                result.append(content)
                result_placeholder.markdown("".join(result))
    
    # Determinar si la respuesta es correcta
    full_result = "".join(result)
    is_correct = "CORRECTO" in full_result
    
    return is_correct, full_result

def clue_assistant(client, deployment_name, clues, question_text, clue_index=None, user_query=None):
    """
    Agente ClueAssistant para dar pistas y ayuda.
    
    Args:
        client: Cliente de AzureOpenAI
        deployment_name: Nombre del modelo desplegado
        clues: Lista de pistas disponibles
        question_text: Texto de la pregunta actual
        clue_index: Índice de la última pista revelada
        user_query: Consulta específica del usuario (opcional)
        
    Returns:
        str: Respuesta del asistente
    """
    # Texto de pistas disponibles
    clues_text = "\n".join([f"Pista {i+1}: {clue}" for i, clue in enumerate(clues[:clue_index+1])]) if clue_index is not None else ""
    
    # Base del prompt
    prompt = f"""
    Sistema: Sos un asistente amigable para un juego de acertijos para una señora argentina de 70 años llamada Claude.
    Tu nombre es "El Genio" y tu labor es ayudarla a descubrir las respuestas a través de pistas.
    Habla con calidez y paciencia, usando modismos argentinos ocasionalmente.
    Adaptá tu lenguaje para que sea fácil de entender para una persona mayor.
    
    La pregunta actual es: "{question_text}"
    
    Las pistas disponibles son:
    {clues_text}
    """
    
    # Adaptar el prompt según si hay una consulta específica
    if user_query and user_query.strip():
        prompt += f"""
        Claude te ha preguntado: "{user_query}"
        
        Responde directamente a su pregunta, dándole ayuda relacionada con el acertijo sin revelarle
        la respuesta directamente. Sé amable y paciente, explicando las cosas de manera clara.
        Si su pregunta no está relacionada con el acertijo actual, puedes responder brevemente
        pero recuérdale amablemente que tu función es ayudarla a resolver el acertijo actual.
        """
    else:
        prompt += """
        Proporcioná una explicación amable de las pistas disponibles, dándole un poco más de contexto
        sin revelar directamente la respuesta. Animate a contar alguna anécdota relacionada
        para hacer la experiencia más personal y entretenida.
        """

    # Llamada al modelo con streaming
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": prompt}
        ],
        temperature=0.9,
        max_tokens=500,
        stream=True
    )
    
    # Mostrar animación de carga
    result_placeholder = st.empty()
    result_placeholder.markdown(loading_animation_html(), unsafe_allow_html=True)
    
    # Procesar respuesta streaming
    result = []
    
    for chunk in response:
        if chunk.choices:
            content = chunk.choices[0].delta.content
            if content:
                result.append(content)
                result_placeholder.markdown("".join(result))
    
    return "".join(result)