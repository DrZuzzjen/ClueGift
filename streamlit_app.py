"""
Regalo Misterioso - Versión 2 - Estado completamente en memoria
Una aplicación de acertijos con IA para una experiencia de regalo de cumpleaños.
"""
import os
import time
import yaml
from dotenv import load_dotenv
import streamlit as st

# Importar módulos refactorizados
from style import load_css, reset_button_js, loading_animation_html
from llm_agents import initialize_client, answer_grader, clue_assistant

# Cargar variables de entorno
load_dotenv()

# Constantes para claves de session_state
KEY_INITIALIZED = "initialized"
KEY_CURRENT_QUESTION_ID = "current_question_id"
KEY_COMPLETED_QUESTIONS = "completed_questions"
KEY_REVEALED_CLUES = "revealed_clues" 
KEY_FEEDBACK = "feedback"
KEY_IS_CORRECT = "is_correct"
KEY_SUBMITTED = "submitted"
KEY_GENIUS_RESPONSE = "genius_response"
KEY_SHOW_GENIUS = "show_genius"
KEY_GAME_COMPLETED = "game_completed"
KEY_PENDING_GENIUS_QUERY = "pending_genius_query"

@st.dialog("Mensaje del Genio 🧞‍♂️", width="large")
def genius_dialog(message):
    """Diálogo modal para mostrar mensajes del Genio."""
    st.markdown("""
        <div style='text-align: center; margin-bottom: 1rem;'>
            <span style='font-size: 4rem;'>🧞‍♂️</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='background: rgba(147, 112, 219, 0.2); padding: 20px; border-radius: 10px; margin: 1rem 0;'>
            {message}
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("✨ Entendido", type="primary", use_container_width=True):
        st.session_state[KEY_SHOW_GENIUS] = False
        st.rerun()

def load_clues():
    """Cargar las preguntas y respuestas desde el archivo YAML."""
    with open("clues.yaml", 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def initialize_session():
    """Inicializar el estado de la sesión si es necesario."""
    if KEY_INITIALIZED not in st.session_state:
        st.session_state[KEY_INITIALIZED] = True
        st.session_state[KEY_CURRENT_QUESTION_ID] = 1
        st.session_state[KEY_COMPLETED_QUESTIONS] = []
        st.session_state[KEY_REVEALED_CLUES] = []
        st.session_state[KEY_FEEDBACK] = ""
        st.session_state[KEY_IS_CORRECT] = False
        st.session_state[KEY_SUBMITTED] = False
        st.session_state[KEY_GENIUS_RESPONSE] = ""
        st.session_state[KEY_SHOW_GENIUS] = False
        st.session_state[KEY_GAME_COMPLETED] = False
        st.session_state[KEY_PENDING_GENIUS_QUERY] = None
        # Eliminamos la entrada user_input para evitar problemas con el widget
        if "user_input" in st.session_state:
            del st.session_state["user_input"]

def reset_game():
    """Reiniciar todo el juego."""
    st.session_state[KEY_CURRENT_QUESTION_ID] = 1
    st.session_state[KEY_COMPLETED_QUESTIONS] = []
    st.session_state[KEY_REVEALED_CLUES] = []
    st.session_state[KEY_FEEDBACK] = ""
    st.session_state[KEY_IS_CORRECT] = False
    st.session_state[KEY_SUBMITTED] = False
    st.session_state[KEY_GENIUS_RESPONSE] = ""
    st.session_state[KEY_SHOW_GENIUS] = False
    st.session_state[KEY_GAME_COMPLETED] = False
    # Eliminamos la entrada user_input para evitar problemas con el widget
    if "user_input" in st.session_state:
        del st.session_state["user_input"]
    st.rerun()

def get_current_question(clues_data):
    """Obtener la pregunta actual basada en el ID almacenado en la sesión."""
    current_id = st.session_state[KEY_CURRENT_QUESTION_ID]
    
    for question in clues_data["questions"]:
        if question["id"] == current_id:
            return question
            
    return None

def advance_to_next_question():
    """Avanzar a la siguiente pregunta."""
    st.session_state[KEY_CURRENT_QUESTION_ID] += 1
    st.session_state[KEY_REVEALED_CLUES] = []
    st.session_state[KEY_SUBMITTED] = False
    st.session_state[KEY_FEEDBACK] = ""
    if "user_input" in st.session_state:
        del st.session_state["user_input"]

def get_credentials():
    """Obtener credenciales para la API de Azure OpenAI."""
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

def main():
    # Configurar la página
    st.set_page_config(
        page_title="Regalo Misterioso 🎁",
        page_icon="🎁",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Usar el tema oscuro
    st.markdown("""
        <style>
            [data-testid="stAppViewContainer"] {
                background: linear-gradient(135deg, #2a0845, #6441A5);
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Cargar estilos CSS
    load_css()
    
    # Botón de reinicio (arriba a la derecha)
    reset_button_js()
    
    # Inicializar el estado de la sesión
    initialize_session()
    
    # Verificar si se solicitó un reinicio
    if 'reset' in st.query_params and st.query_params['reset'] == 'true':
        reset_game()
        st.query_params.clear()
    
    # Obtener credenciales
    api_key, endpoint, api_version, deployment_name = get_credentials()
    
    # Inicializar el cliente de OpenAI para Azure
    client = initialize_client(api_key, api_version, endpoint)
    
    # Cargar datos
    clues_data = load_clues()
    
    # PRIMERO: Verificar si hay una consulta pendiente al genio
    if st.session_state.get(KEY_PENDING_GENIUS_QUERY) is not None:
        # Mostrar SOLO un spinner a pantalla completa y nada más
        with st.spinner("El Genio está pensando..."):
            current_question = get_current_question(clues_data)
            
            # Obtener pistas reveladas para el asistente
            revealed_clues_content = []
            for i in st.session_state[KEY_REVEALED_CLUES]:
                if i < len(current_question['clues']):
                    revealed_clues_content.append(current_question['clues'][i])
            
            # Obtener respuesta del Genio
            user_query = st.session_state[KEY_PENDING_GENIUS_QUERY]
            genius_response = clue_assistant(
                client,
                deployment_name,
                current_question['clues'],
                current_question['question'],
                len(revealed_clues_content) - 1 if revealed_clues_content else -1,
                user_query
            )
            
            # Guardar la respuesta y limpiar la consulta pendiente
            st.session_state[KEY_GENIUS_RESPONSE] = genius_response
            st.session_state[KEY_SHOW_GENIUS] = True
            st.session_state[KEY_PENDING_GENIUS_QUERY] = None

        # Mostrar el diálogo inmediatamente después de obtener la respuesta
        if st.session_state[KEY_SHOW_GENIUS] and st.session_state[KEY_GENIUS_RESPONSE]:
            genius_dialog(st.session_state[KEY_GENIUS_RESPONSE])
            # No hacer rerun aquí para evitar bucles
        
        # Detener la ejecución aquí para no mostrar el resto de la interfaz
        st.stop()
    
    # RESTO DEL CÓDIGO NORMAL (solo se ejecuta si no hay consulta pendiente)
    # Título y bienvenida
    st.title(" 🎁Regalo Misterioso")
    #st.markdown("<h3 class='subtitle'>¡Bienvenida Claude! ¿Estás lista para el desafío? 🔍🕵️‍♀️ </h3>", unsafe_allow_html=True)
    
    # Mensaje de bienvenida si no hay preguntas completadas
    if not st.session_state[KEY_COMPLETED_QUESTIONS]:
        st.markdown("""
        <div class="welcome-box">
            <h3>¡Bienvenida, Claude! 👋</h3>
            <h5>¡Bienvenida Claude! ¿Estás lista para el desafío? 🔍🕵️‍♀️ </h5>
            <p>Te espera una aventura llena de misterios y acertijos. Cada respuesta correcta te acercará más a descubrir tu regalo de cumpleaños.</p>
            <p>¿Estás lista para comenzar este viaje de recuerdos? El Genio estará aquí para ayudarte si necesitás una mano.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Verificar si el juego se ha completado
    if len(st.session_state[KEY_COMPLETED_QUESTIONS]) >= clues_data["total_questions"]:
        if not st.session_state[KEY_GAME_COMPLETED]:
            st.session_state[KEY_GAME_COMPLETED] = True
            
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
    current_question = get_current_question(clues_data)
    
    if not current_question:
        st.error("¡Ups! No se pudo encontrar la pregunta actual. Por favor, reinicia la aplicación.")
        return
    
    # Mostrar información sobre el progreso
    progress_text = f"Acertijo {current_question['id']} de {clues_data['total_questions']}"
    st.progress(float(current_question['id']) / float(clues_data['total_questions']))
    st.markdown(f"<p style='text-align: center;'>{progress_text}</p>", unsafe_allow_html=True)
    
    # Si hay un mensaje del Genio para mostrar
    if st.session_state[KEY_SHOW_GENIUS] and st.session_state[KEY_GENIUS_RESPONSE]:
        genius_dialog(st.session_state[KEY_GENIUS_RESPONSE])
        # Reset the flag immediately after showing the dialog
        st.session_state[KEY_SHOW_GENIUS] = False
        
   # Mostrar la pregunta actual
    st.markdown(f"""
    <div class="highlight">
        <h2>Pregunta:</h2>
        <p>{current_question['question']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sección para pistas
    # Sección para pistas
    st.markdown("### Pistas disponibles:")
    
    # Mostrar indicadores de pistas disponibles
    max_clues = len(current_question.get('clues', []))
    
    # Crear un contenedor flexible para los indicadores
    st.markdown('<div class="clue-indicators">', unsafe_allow_html=True)
    
    # Crear columnas en una sola fila para los indicadores
    cols = st.columns(max_clues)
    for i, col in enumerate(cols):
        with col:
            # Determinar si esta pista está encendida o apagada
            is_revealed = i in st.session_state[KEY_REVEALED_CLUES]
            is_next = i == len(st.session_state[KEY_REVEALED_CLUES])
            
            css_class = "clue-on" if is_revealed else "clue-off"
            
            # Solo habilitar clic para la siguiente pista disponible
            if is_next:
                if st.button("💡", key=f"clue_{i}"):
                    st.session_state[KEY_REVEALED_CLUES].append(i)
                    st.rerun()
            else:
                st.markdown(f'<div class="clue-container"><span class="clue-bulb {css_class}">💡</span></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Mostrar pistas ya reveladas
    if st.session_state[KEY_REVEALED_CLUES]:
        for i in st.session_state[KEY_REVEALED_CLUES]:
            if i < max_clues:
                st.markdown(f"""
                <div class="clue-box">
                    <p>🔍 {current_question['clues'][i]}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Área para ingresar respuesta
    st.markdown("### Tu respuesta:")
    
    # Usamos una key única para el formulario basada en la pregunta actual
    # para evitar problemas de estado persistente entre preguntas
    form_key = f"form_{current_question['id']}"
    
    with st.form(form_key):
        # Usamos una key única para el input basada en la pregunta actual
        input_key = f"input_{current_question['id']}"
        user_answer = st.text_input(
            "Escribe tu respuesta aquí o una pregunta para El Genio:",
            key=input_key
        )
        
        submit_col1, submit_col2 = st.columns(2)
        
        with submit_col1:
            submit_button = st.form_submit_button("Enviar respuesta ✅")
        
        with submit_col2:
            help_button = st.form_submit_button("Consultar al Genio 🧞‍♂️")
    
    # Procesar envío de respuesta - ESTE ES EL FLUJO CRÍTICO
    if submit_button and user_answer:
        # Reiniciar TODOS los estados relacionados con el genio
        st.session_state[KEY_SHOW_GENIUS] = False
        st.session_state[KEY_GENIUS_RESPONSE] = ""
        
        # Evaluar la respuesta
        is_correct, feedback = answer_grader(
            client, 
            deployment_name, 
            user_answer, 
            current_question['answer'], 
            current_question['question']
        )
        
        # Verificación adicional para asegurarse de que la respuesta está correctamente clasificada
        feedback_text = feedback.strip()
        is_correct = feedback_text.startswith("CORRECTO")
        
        # Guardar el resultado y feedback
        st.session_state[KEY_IS_CORRECT] = is_correct
        st.session_state[KEY_FEEDBACK] = feedback
        st.session_state[KEY_SUBMITTED] = True
        st.snow()
        
        # SOLO si es correcta, avanzar a la siguiente pregunta
        if is_correct:
            # Agregar a preguntas completadas y avanzar
            if current_question['id'] not in st.session_state[KEY_COMPLETED_QUESTIONS]:
                st.session_state[KEY_COMPLETED_QUESTIONS].append(current_question['id'])
            
            # Efecto de celebración con mensaje y pequeña pausa
            st.balloons()
            
            # Agregar un mensaje de éxito para confirmar visualmente
            st.success("¡Respuesta correcta! Avanzando al siguiente acertijo...")
            
            # Pequeña pausa para dar tiempo a que se muestren los globos
            import time
            time.sleep(1.5)
            
            # Avanzar a la siguiente pregunta
            advance_to_next_question()
            st.rerun()

    # Procesar solicitud de ayuda al Genio
    if help_button and user_answer:
        # Limpiar cualquier estado previo del genio
        st.session_state[KEY_SHOW_GENIUS] = False
        st.session_state[KEY_GENIUS_RESPONSE] = ""
        
        # Obtener pistas reveladas para el asistente
        revealed_clues_content = []
        for i in st.session_state[KEY_REVEALED_CLUES]:
            if i < len(current_question['clues']):
                revealed_clues_content.append(current_question['clues'][i])
        
        # Obtener respuesta del Genio (ahora sin streaming visible)
        genius_response = clue_assistant(
            client,
            deployment_name,
            current_question['clues'],
            current_question['question'],
            len(revealed_clues_content) - 1 if revealed_clues_content else -1,
            user_answer
        )
        
        # Guardar la respuesta del Genio y activar su visualización
        st.session_state[KEY_GENIUS_RESPONSE] = genius_response
        st.session_state[KEY_SHOW_GENIUS] = True
        st.rerun()

if __name__ == "__main__":
    main()