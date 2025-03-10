"""
Módulo para contener el CSS personalizado usado en la aplicación Regalo Misterioso.
"""
import streamlit as st

def load_css():
    """Cargar el CSS personalizado para la aplicación."""
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

def reset_button_js():
    """Agregar JS para el botón de reinicio."""
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

def loading_animation_html():
    """HTML para la animación de carga."""
    return """
    <div class="loading">
        <div class="loading-dot loading-dot-1"></div>
        <div class="loading-dot loading-dot-2"></div>
        <div class="loading-dot loading-dot-3"></div>
    </div>
    """