import os
import yaml
import json
import streamlit as st
import time
from datetime import datetime
from openai import AzureOpenAI
from dotenv import load_dotenv

# Cargar variables de entorno (para desarrollo local)
load_dotenv()

# Configuración de página de Streamlit
st.set_page_config(
    page_title="Regalo Misterioso 🎁",
    page_icon="🎁",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Estilos CSS personalizados
st.markdown("""
<style>
    /* Fondo para toda la página */
    .stApp {
        background: linear-gradient(135deg, #2a0845, #6441A5);
        max-width: 100%;
    }
    
    /* Hacer el contenedor principal transparente */
    .main .block-container {
        background-color: transparent;
        color: white;
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Estilos para encabezados */
    h1, h2, h3 {
        color: #FFD700;
        font-family: 'Palatino Linotype', serif;
    }
    
    /* Estilos para botones normales */
    .stButton>button {
        background-color: #9370DB;
        color: white;
        border-radius: 20px;
        padding: 10px 24px;
        transition: all 0.3s ease;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #7B68EE;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Estilos para el botón de reseteo */
    .reset-button {
        position: absolute;
        top: 10px;
        right: 10px;
        background-color: #FF6347;
        color: white;
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        font-size: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        z-index: 1000;
    }
    .reset-button:hover {
        background-color: #FF4500;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Cajas decorativas */
    .highlight {
        background: rgba(255, 215, 0, 0.2);
        padding: 10px;
        border-radius: 10px;
        border-left: 5px solid #FFD700;
        margin-bottom: 20px;
    }
    .clue-box {
        background: rgba(147, 112, 219, 0.2);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .answer-area {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    
    /* Animaciones */
    .emoji-large {
        font-size: 28px;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    .pulse {
        animation: pulse 2s infinite;
        display: inline-block;
    }
    
    /* Cajas informativas */
    .welcome-box {
        background: rgba(255, 215, 0, 0.1);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        border: 1px solid rgba(255, 215, 0, 0.3);
    }
    .success-box {
        background: rgba(72, 209, 204, 0.2);
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        border-left: 5px solid #48D1CC;
    }
    
    /* Animación de carga */
    .loading {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
    }
    .loading-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background-color: #FFD700;
        margin: 0 5px;
        display: inline-block;
    }
    .loading-dot-1 {
        animation: jump 1.5s ease-in-out infinite;
    }
    .loading-dot-2 {
        animation: jump 1.5s ease-in-out 0.25s infinite;
    }
    .loading-dot-3 {
        animation: jump 1.5s ease-in-out 0.5s infinite;
    }
    @keyframes jump {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-15px); }
    }
</style>
""", unsafe_allow_html=True)

# Obtener credenciales (primero de secrets de Streamlit, luego de variables de entorno)
def get_credentials():
    try:
        # Intentar obtener de secrets de Streamlit (para despliegue)
        api_key = st.secrets["azure_openai"]["AZURE_OPENAI_API_KEY"]
        endpoint = st.secrets["azure_openai"]["AZURE_OPENAI_ENDPOINT"]
        api_version = st.secrets["azure_openai"]["OPENAI_API_VERSION"]
        deployment_name = st.secrets["azure_openai"]["AZURE_OPENAI_DEPLOYMENT_NAME"]
    except Exception as e:
        # Fallback a variables de entorno (para desarrollo local)
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_version = os.getenv("OPENAI_API_VERSION")
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    return api_key, endpoint, api_version, deployment_name

# Obtener credenciales
api_key, endpoint, api_version, deployment_name = get_credentials()

# Inicializar el cliente de OpenAI para Azure
client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=endpoint
)

# Función para cargar las pistas desde el archivo YAML
def load_clues():
    with open("clues.yaml", 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

# Función para cargar el progreso desde el archivo YAML
def load_progress():
    try:
        with open("progress.yaml", 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        # Si el archivo no existe, devolver valores predeterminados
        return {"completed_questions": [], "current_question": 1, "clues_revealed": 0}

# Función para guardar el progreso en el archivo YAML
def save_progress(progress_data):
    with open("progress.yaml", 'w', encoding='utf-8') as file:
        yaml.dump(progress_data, file)

# Función para reiniciar el progreso
def reset_progress():
    progress_data = {"completed_questions": [], "current_question": 1, "clues_revealed": 0}
    save_progress(progress_data)
    return progress_data

# Función para obtener la pregunta actual
def get_current_question(clues_data, progress_data):
    current_id = progress_data["current_question"]
    for question in clues_data["questions"]:
        if question["id"] == current_id:
            return question
    return None

# Función para la animación de carga
def loading_animation():
    with st.container():
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        with col3:
            st.markdown("""
            <div class="loading">
                <div class="loading-dot loading-dot-1"></div>
                <div class="loading-dot loading-dot-2"></div>
                <div class="loading-dot loading-dot-3"></div>
            </div>
            """, unsafe_allow_html=True)

# Agente AnswerGrader para evaluar las respuestas
def answer_grader(user_answer, correct_answer, question):
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

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=150,
        stream=True
    )
    
    # Preparar para streaming
    result = []
    result_placeholder = st.empty()
    
    for chunk in response:
        if chunk.choices:
            content = chunk.choices[0].delta.content
            if content:
                result.append(content)
                result_placeholder.markdown("".join(result))
    
    full_result = "".join(result)
    is_correct = "CORRECTO" in full_result
    
    return is_correct, full_result

# Agente ClueAssistant para dar pistas y ayuda
def clue_assistant(clues, question_text, clue_index=None, user_query=None):
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
    
    # Si el usuario hizo una pregunta específica, responder a esa pregunta
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

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": prompt}
        ],
        temperature=0.9,
        max_tokens=500,
        stream=True
    )
    
    # Preparar para streaming
    result = []
    result_placeholder = st.empty()
    
    for chunk in response:
        if chunk.choices:
            content = chunk.choices[0].delta.content
            if content:
                result.append(content)
                result_placeholder.markdown("".join(result))
    
    return "".join(result)

# Función principal de la aplicación
def main():
    # Cargar datos
    clues_data = load_clues()
    progress_data = load_progress()
    
    # Inicializar session_state si es necesario
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.showing_clue = False
        st.session_state.last_clue_index = progress_data["clues_revealed"]
        st.session_state.answer_submitted = False
        st.session_state.answer_correct = False
        st.session_state.answer_feedback = ""
        st.session_state.need_genius_help = False
        st.session_state.genius_response = ""
        st.session_state.game_completed = False
    
    # Botón de reinicio (arriba a la derecha)
    reset_col = st.container()
    with reset_col:
        st.markdown("""
        <div style="position: fixed; top: 10px; right: 10px; z-index: 1000;">
            <button id="reset-button" class="reset-button" title="Reiniciar juego">🔄</button>
        </div>
        <script>
            document.getElementById('reset-button').addEventListener('click', function() {
                if(confirm('¿Estás segura de que quieres reiniciar el juego? Perderás todo tu progreso.')) {
                    window.location.href = '?reset=true';
                }
            });
        </script>
        """, unsafe_allow_html=True)
    
    # Verificar si se solicitó un reinicio (a través del querystring)
    query_params = st.experimental_get_query_params()
    if 'reset' in query_params and query_params['reset'][0] == 'true':
        progress_data = reset_progress()
        st.session_state.last_clue_index = 0
        st.session_state.answer_submitted = False
        st.session_state.answer_correct = False
        st.session_state.answer_feedback = ""
        st.session_state.need_genius_help = False
        st.session_state.genius_response = ""
        st.session_state.game_completed = False
        st.experimental_set_query_params()  # Limpiar el querystring
        
    # Título y bienvenida
    col1, col2 = st.columns([1, 9])
    with col1:
        st.markdown('<span class="emoji-large pulse">🎁</span>', unsafe_allow_html=True)
    with col2:
        st.title("Regalo Misterioso")

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
            <p>Has completado todos los acertijos exitosamente.</p>
            <p>Tu regalo de cumpleaños te espera en el tercer cajón del mueble del living, envuelto en papel dorado.</p>
            <p>¡Muchísimas felicidades en este día tan especial!</p>
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
    
    # Control de revelación de pistas
    max_clues = len(current_question['clues'])
    clues_revealed = min(st.session_state.last_clue_index + 1, max_clues)
    
    for i in range(clues_revealed):
        st.markdown(f"""
        <div class="clue-box">
            <p>🔍 {current_question['clues'][i]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Botón para revelar más pistas si están disponibles
    if clues_revealed < max_clues and not st.session_state.answer_correct:
        if st.button("Revelar otra pista 🔎"):
            st.session_state.last_clue_index += 1
            progress_data["clues_revealed"] = st.session_state.last_clue_index
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
        loading_animation()
        
        is_correct, feedback = answer_grader(user_answer, current_question['answer'], current_question['question'])
        st.session_state.answer_correct = is_correct
        st.session_state.answer_feedback = feedback
        
        if is_correct:
            # Actualizar progreso
            progress_data["completed_questions"].append(current_question['id'])
            progress_data["current_question"] = current_question['id'] + 1
            progress_data["clues_revealed"] = 0
            save_progress(progress_data)
            
            st.session_state.last_clue_index = 0
            time.sleep(2)  # Pausa para celebración
            st.balloons()
            st.rerun()
    
    # Procesar solicitud de ayuda al Genio
    if help_button:
        st.session_state.need_genius_help = True
        st.session_state.answer_submitted = False
    
    # Mostrar retroalimentación de respuesta
    if st.session_state.answer_submitted:
        st.markdown(f"""
        <div class="{'success-box' if st.session_state.answer_correct else 'clue-box'}">
            <p>{st.session_state.answer_feedback}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Mostrar ayuda del Genio
    if st.session_state.need_genius_help:
        st.markdown("### El Genio dice...")
        loading_animation()
        
        # Pasamos la consulta del usuario al Genio
        genius_response = clue_assistant(
            current_question['clues'], 
            current_question['question'],
            st.session_state.last_clue_index,
            user_answer # Pasar la consulta del usuario
        )
        
        st.session_state.genius_response = genius_response

# Ejecutar la aplicación
if __name__ == "__main__":
    main()