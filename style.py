"""
Módulo para contener el CSS personalizado usado en la aplicación Regalo Misterioso.
"""
import streamlit as st

def load_css():
    """Cargar el CSS personalizado para la aplicación."""
    st.markdown("""
    <style>
        /* Ocultar el menú principal de Streamlit para evitar errores de ARIA */
        .stMainMenu {
            visibility: hidden;
            display: none;
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
        
        /* Estilos para el botón de reseteo - mejorado para mayor visibilidad */
        .reset-button {
            position: fixed !important;
            top: 20px !important;
            right: 20px !important;
            background-color: #FF6347 !important;
            color: white !important;
            border: none !important;
            border-radius: 50% !important;
            width: 45px !important;
            height: 45px !important;
            font-size: 24px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            z-index: 99999 !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        .reset-button:hover {
            background-color: #FF4500 !important;
            transform: translateY(-2px) scale(1.1) !important;
            box-shadow: 0 6px 20px rgba(0,0,0,0.6) !important;
        }

        /* Centrar elementos en columnas */
        [data-testid="column"] {
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /* Estilo simple para indicadores de pistas */
        .clue-indicators {
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            gap: 20px;
            margin: 20px 0;
            width: 100%;
        }
        
        .clue-container {
            display: inline-block;
            text-align: center;
        }
        
        .clue-bulb {
            font-size: 28px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .clue-on {
            color: #FFD700;
            text-shadow: 0 0 10px #FFD700;
        }
        
        .clue-off {
            color: rgba(255,215,0,0.3);
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
        
        /* NUEVO: Estilo simplificado para indicadores de pistas */
        .clue-indicators {
            display: flex;
            justify-content: center;
            margin: 20px 0;
            gap: 15px;
        }
        
        .clue-indicator {
            width: 50px;
            height: 50px;
            font-size: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            background: rgba(147, 112, 219, 0.1);
            border: 2px solid rgba(255,215,0,0.2);
            transition: all 0.3s ease;
            position: relative;
        }
        
        .clue-indicator-on {
            color: #FFD700;
            background: rgba(147, 112, 219, 0.2);
            border-color: rgba(255,215,0,0.5);
            box-shadow: 0 0 10px rgba(255,215,0,0.5);
        }
        
        .clue-indicator-off {
            color: rgba(255,215,0,0.3);
        }
        
        .clue-indicator-btn {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            cursor: pointer;
            opacity: 0;
            z-index: 2;
        }
        
        /* Botón de revelar pista */
        .reveal-clue-btn {
            text-align: center;
            margin: 15px 0;
        }
        .hidden-clue {
            background: rgba(147, 112, 219, 0.1);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            border: 2px dashed rgba(255,215,0,0.3);
            text-align: center;
            cursor: pointer;
        }
        .hidden-clue:hover {
            background: rgba(147, 112, 219, 0.2);
            border: 2px dashed rgba(255,215,0,0.5);
        }
        
        /* Estilos para el modal del Genio */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.7);
            z-index: 1001;
            justify-content: center;
            align-items: center;
            backdrop-filter: blur(5px);
        }
        
        .modal-content {
            background: linear-gradient(135deg, #3a1c59, #4a0d67);
            color: white;
            padding: 25px;
            border-radius: 15px;
            max-width: 600px;
            width: 80%;
            max-height: 80vh;
            overflow-y: auto;
            box-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
            border: 2px solid rgba(147, 112, 219, 0.5);
            position: relative;
            animation: modalAppear 0.3s ease-out;
        }
        
        @keyframes modalAppear {
            from {
                opacity: 0;
                transform: translateY(-50px) scale(0.9);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            border-bottom: 1px solid rgba(255, 215, 0, 0.3);
            padding-bottom: 10px;
        }
        
        .modal-title {
            color: #FFD700;
            margin: 0;
            display: flex;
            align-items: center;
            font-size: 1.5rem;
        }
        
        .modal-title .emoji {
            font-size: 2rem;
            margin-right: 10px;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        .modal-close {
            background-color: transparent;
            color: rgba(255,255,255,0.7);
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .modal-close:hover {
            color: #FFD700;
            transform: scale(1.2);
        }
        
        .modal-body {
            margin-bottom: 20px;
        }
        
        .modal-footer {
            display: flex;
            justify-content: flex-end;
            border-top: 1px solid rgba(255, 215, 0, 0.3);
            padding-top: 15px;
        }
        
        .modal-btn {
            background-color: #9370DB;
            color: white;
            border: none;
            padding: 8px 20px;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: bold;
        }
        
        .modal-btn:hover {
            background-color: #7B68EE;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        /* Estilo para el genio flotante */
        .genius-float {
            position: fixed;
            bottom: 20px;
            right: 20px;
            font-size: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
            z-index: 1000;
            filter: drop-shadow(0 0 10px rgba(255,215,0,0.5));
            animation: float 3s ease-in-out infinite;
        }
        
        .genius-float:hover {
            transform: scale(1.2) translateY(-5px);
        }
    </style>
    """, unsafe_allow_html=True)

def reset_button_js():
    """Agregar JS para el botón de reinicio."""
    st.markdown("""
    <div style="position: fixed; top: 20px; right: 20px; z-index: 99999;">
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

def loading_animation_html():
    """HTML para la animación de carga."""
    return """
    <div class="loading">
        <div class="loading-dot loading-dot-1"></div>
        <div class="loading-dot loading-dot-2"></div>
        <div class="loading-dot loading-dot-3"></div>
    </div>
    """

def genius_modal_html(genius_response=""):
    """HTML y JavaScript para el modal del Genio."""
    return f"""
    <div id="geniusModal" class="modal-overlay">
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title"><span class="emoji">🧞</span> Mensaje del Genio</h2>
                <button class="modal-close" onclick="closeGeniusModal()">&times;</button>
            </div>
            <div class="modal-body">
                <p>{genius_response}</p>
            </div>
            <div class="modal-footer">
                <button class="modal-btn" onclick="closeGeniusModal()">Cerrar</button>
            </div>
        </div>
    </div>

    <script>
        // Función para cerrar el modal
        function closeGeniusModal() {{
            document.getElementById('geniusModal').style.display = 'none';
        }}
        
        // Función para mostrar el modal
        function openGeniusModal() {{
            document.getElementById('geniusModal').style.display = 'flex';
        }}
        
        // Mostrar el modal automáticamente si hay un mensaje
        document.addEventListener('DOMContentLoaded', function() {{
            const geniusResponse = `{genius_response}`;
            if (geniusResponse && geniusResponse.trim() !== '') {{
                setTimeout(openGeniusModal, 500);
            }}
        }});
        
        // Cerrar el modal al hacer clic fuera de su contenido
        document.getElementById('geniusModal').addEventListener('click', function(e) {{
            if (e.target === this) {{
                closeGeniusModal();
            }}
        }});
    </script>
    """
