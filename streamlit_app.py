"""
Regalo Misterioso - Una aplicación de acertijos con IA para una experiencia de regalo de cumpleaños.
"""
import os
import time
from datetime import datetime
from dotenv import load_dotenv
import streamlit as st

# Importar módulos refactorizados
from style import load_css, reset_button_js, loading_animation_html
from llm_agents import initialize_client, answer_grader, clue_assistant
from game_manager import (
    load_clues, load_progress, save_progress, 
    reset_progress, get_current_question
)

# Cargar variables de entorno (para desarrollo local)
load_dotenv()

# Configuración de página de Streamlit
st.set_page_config(
    page_title="Regalo Misterioso 🎁",
    page_icon="🎁",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Cargar estilos CSS
load_css()

# Obtener credenciales (primero de secrets de Streamlit, luego de variables de entorno)
def get_credentials():
    try:
        # Intentar obtener de secrets de Streamlit (para despliegue)
        api_key = st.secrets["azure_openai"]["AZURE_OPENAI_API_KEY"]
        endpoint = st.secrets["azure_openai"]["AZURE_OPENAI_ENDPOINT"]
        api_version = st.secrets["azure_openai"]["OPENAI_API_VERSION"]
        deployment_name = st.secrets["azure_openai"]["AZURE_OPENAI_DEPLOYMENT_NAME"]
    except Exception:
        # Fallback a variables de entorno (para desarrollo local)
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_version = os.getenv("OPENAI_API_VERSION")
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    return api_key, endpoint, api_version, deployment_name

# Función para mostrar la animación de carga
def display_loading_animation():
    with st.container():
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        with col3:
            st.markdown(loading_animation_html(), unsafe_allow_html=True)

# Función principal de la aplicación
def main():
    # Obtener credenciales
    api_key, endpoint, api_version, deployment_name = get_credentials()
    
    # Inicializar el cliente de OpenAI para Azure
    client = initialize_client(api_key, api_version, endpoint)
    
    # Cargar datos
    clues_data = load_clues()
    progress_data = load_progress()
    
    # Inicializar session_state si es necesario
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.showing_clue = False
        st.session_state.last_clue_index = -1  # Cambiado a -1 para que no se revele ninguna pista inicialmente
        st.session_state.revealed_clues = []  # Nueva lista para rastrear pistas reveladas
        st.session_state.answer_submitted = False
        st.session_state.answer_correct = False
        st.session_state.answer_feedback = ""
        st.session_state.need_genius_help = False
        st.session_state.genius_response = ""
        st.session_state.game_completed = False
    
    # Botón de reinicio (arriba a la derecha)
    reset_button_js()
    
    # Verificar si se solicitó un reinicio (a través del querystring)
    if 'reset' in st.query_params and st.query_params['reset'] == 'true':
        progress_data = reset_progress()
        st.session_state.last_clue_index = -1
        st.session_state.revealed_clues = []
        st.session_state.answer_submitted = False
        st.session_state.answer_correct = False
        st.session_state.answer_feedback = ""
        st.session_state.need_genius_help = False
        st.session_state.genius_response = ""
        st.session_state.game_completed = False
        # Limpiar el querystring
        st.query_params.clear()  
        st.rerun()
        
    # Título y bienvenida
    st.title(" 🎁Regalo Misterioso")
    st.markdown("<h3 class='subtitle'>¡Bienvenida Claude! ¿Estás lista para el desafío? 🔍🕵️‍♀️ </h3>", unsafe_allow_html=True)

    # Mensaje de bienvenida
    if not progress_data["completed_questions"]:
        st.markdown("""
        <div class="welcome-box">
            <h3>¡Bienvenida, Claude! 👋</h3>
            <p>Te espera una aventura llena de misterios y acertijos. Cada respuesta correcta te acercará más a descubrir tu regalo de cumpleaños.</p>
            <p>¿Estás lista para comenzar este viaje de recuerdos? El Genio estará aquí para ayudarte si necesitás una mano.</p>
        </div>
        """, unsafe_allow_html=True)

    # Verificar si el juego se ha completado
    if len(progress_data["completed_questions"]) >= clues_data["total_questions"]:
        if not st.session_state.game_completed:
            st.session_state.game_completed = True
            
        st.markdown("""
        <div class="success-box">
            <h2>¡Felicitaciones! 🎉</h2>
            <p>¡Has completado todos los acertijos exitosamente! 🌟</p>
            <h3>Información importante sobre tu regalo 🎁</h3>
            <p>Por favor prepara:</p>
            <ul>
            <li>🧳 Una maleta pequeña con ropa para 3 días</li>
            <li>👗 Ropa elegante y cómoda (no de gala)</li>
            <li>🏊‍♀️ Tu bañador/traje de baño</li>
            <li>⛳ Tu kit completo de golf y ropa de golf</li>
            </ul>
            <h3>Punto de encuentro 📍</h3>
            <p>🚗 Debes estar en tu coche en la estación de Sens</p>
            <p>📅 El día de tu cumpleaños</p>
            <p>⏰ A las 14:30 horas</p>
            <p>¡Prepárate para una sorpresa inolvidable! ✨</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.balloons()
        return

    # Obtener pregunta actual
    current_question = get_current_question(clues_data, progress_data)
    
    if not current_question:
        st.error("¡Ups! No se pudo encontrar la pregunta actual. Por favor, reinicia la aplicación.")
        return
    
    # Mostrar información sobre el progreso
    progress_text = f"Acertijo {current_question['id']} de {clues_data['total_questions']}"
    st.progress(float(current_question['id']) / float(clues_data['total_questions']))
    st.markdown(f"<p style='text-align: center;'>{progress_text}</p>", unsafe_allow_html=True)

    # Mostrar la pregunta actual
    st.markdown(f"""
    <div class="highlight">
        <h2>Pregunta:</h2>
        <p>{current_question['question']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sección para pistas
    st.markdown("### Pistas disponibles:")
    
    # Mostrar indicadores de pistas disponibles (bombillas)
    max_clues = len(current_question['clues'])
    
    # Crear HTML para los indicadores de pistas
    clue_indicators_html = '<div class="clue-indicators">'
    for i in range(max_clues):
        if i in st.session_state.revealed_clues:
            clue_indicators_html += f'<div class="clue-indicator clue-indicator-on">💡</div>'
        else:
            clue_indicators_html += f'<div class="clue-indicator clue-indicator-off">💡</div>'
    clue_indicators_html += '</div>'
    
    st.markdown(clue_indicators_html, unsafe_allow_html=True)
    
    # Mostrar pistas ya reveladas
    for i in st.session_state.revealed_clues:
        if i < max_clues:
            st.markdown(f"""
            <div class="clue-box">
                <p>🔍 {current_question['clues'][i]}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Botón para revelar una pista
    if len(st.session_state.revealed_clues) < max_clues and not st.session_state.answer_correct:
        next_clue_index = 0
        while next_clue_index in st.session_state.revealed_clues and next_clue_index < max_clues:
            next_clue_index += 1
            
        if next_clue_index < max_clues:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("Revelar pista 💡"):
                    st.session_state.revealed_clues.append(next_clue_index)
                    st.session_state.last_clue_index = next_clue_index
                    progress_data["clues_revealed"] = next_clue_index
                    save_progress(progress_data)
                    st.rerun()
    
    # Área para ingresar respuesta
    st.markdown("### Tu respuesta:")
    with st.form("answer_form"):
        user_answer = st.text_input("Escribe tu respuesta aquí o una pregunta para El Genio:", key="user_input")
        submit_col1, submit_col2 = st.columns(2)
        
        with submit_col1:
            submit_button = st.form_submit_button("Enviar respuesta ✅")
        
        with submit_col2:
            help_button = st.form_submit_button("Consultar al Genio 🧞")
    
    # Procesar envío de respuesta
    if submit_button and user_answer:
        st.session_state.answer_submitted = True
        st.session_state.need_genius_help = False
        
        st.markdown("### Evaluando tu respuesta...")
        
        is_correct, feedback = answer_grader(
            client, 
            deployment_name, 
            user_answer, 
            current_question['answer'], 
            current_question['question']
        )
        
        st.session_state.answer_correct = is_correct
        st.session_state.answer_feedback = feedback
        
        if is_correct:
            # Actualizar progreso
            progress_data["completed_questions"].append(current_question['id'])
            progress_data["current_question"] = current_question['id'] + 1
            progress_data["clues_revealed"] = 0
            save_progress(progress_data)
            
            st.session_state.last_clue_index = -1
            st.session_state.revealed_clues = []
            time.sleep(2)  # Pausa para celebración
            st.balloons()
            st.rerun()
    
    # Procesar solicitud de ayuda al Genio
    if help_button:
        st.session_state.need_genius_help = True
        st.session_state.answer_submitted = False
        
        st.markdown("### El Genio dice:")
        
        # Obtener las pistas reveladas para pasar al asistente
        revealed_clues_content = []
        for i in st.session_state.revealed_clues:
            if i < len(current_question['clues']):
                revealed_clues_content.append(current_question['clues'][i])
        
        # Pasar la consulta del usuario al Genio
        genius_response = clue_assistant(
            client,
            deployment_name,
            current_question['clues'], 
            current_question['question'],
            len(revealed_clues_content) - 1 if revealed_clues_content else -1,
            user_answer  # Pasar la consulta del usuario
        )
        
        st.session_state.genius_response = genius_response
        st.markdown(f"""
        <div class="clue-box">
            <p>{genius_response}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Mostrar retroalimentación de respuesta
    if st.session_state.answer_submitted:
        st.markdown(f"""
        <div class="{'success-box' if st.session_state.answer_correct else 'clue-box'}">
            <p>{st.session_state.answer_feedback}</p>
        </div>
        """, unsafe_allow_html=True)

# Ejecutar la aplicación
if __name__ == "__main__":
    main()