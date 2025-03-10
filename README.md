# Regalo Misterioso 🎁

Una aplicación de acertijos con IA para una experiencia de regalo de cumpleaños especial.

## Descripción

Regalo Misterioso es una aplicación de Streamlit que guía a un usuario a través de una serie de acertijos personalizados, utilizando IA para validar respuestas y proporcionar pistas. Diseñada específicamente para Claude, una mujer argentina de 70 años, esta experiencia interactiva la llevará a descubrir dónde se encuentra su regalo de cumpleaños.

La aplicación incluye:
- Acertijos progresivos que se desbloquean al resolver el anterior
- Un "Genio" asistente que brinda ayuda contextual
- Pistas graduales para cada acertijo
- Evaluación inteligente de respuestas usando Azure OpenAI
- Interfaz amigable con diseño adaptado para usuarios mayores

## Estructura de Archivos

- `app.py` - La aplicación principal de Streamlit
- `clues.yaml` - Contiene los acertijos, respuestas y pistas
- `progress.yaml` - Almacena el progreso del usuario
- `pyproject.toml` - Configuración del proyecto y dependencias
- `.env` - Variables de entorno para desarrollo local (no incluido en el repositorio)
- `.streamlit/secrets.toml` - Configuración de secrets para Streamlit Cloud

## Requisitos

- Python 3.10+
- Streamlit 1.26.0+
- Azure OpenAI API key
- Paquetes adicionales especificados en pyproject.toml

## Configuración Local

1. Clona este repositorio:
```
git clone <url-del-repositorio>
cd regalo-misterioso
```

2. Crea un entorno virtual y actívalo:
```
python -m venv venv
# En Windows
venv\Scripts\activate
# En macOS/Linux
source venv/bin/activate
```

3. Instala las dependencias usando Poetry (recomendado):
```
pip install poetry
poetry install
```

O usando pip directamente:
```
pip install -r requirements.txt
```

4. Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:
```
AZURE_OPENAI_API_KEY=tu_api_key
AZURE_OPENAI_ENDPOINT=tu_endpoint
OPENAI_API_VERSION=2023-05-15
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
```

5. Ejecuta la aplicación:
```
streamlit run app.py
```

## Despliegue en Streamlit Cloud

1. Sube el código a un repositorio de GitHub

2. Inicia sesión en [Streamlit Cloud](https://streamlit.io/cloud)

3. Haz clic en "New app" y selecciona el repositorio

4. En la configuración avanzada, añade los siguientes secrets:
```toml
[azure_openai]
AZURE_OPENAI_API_KEY = "tu_api_key"
AZURE_OPENAI_ENDPOINT = "tu_endpoint"
OPENAI_API_VERSION = "2023-05-15"
AZURE_OPENAI_DEPLOYMENT_NAME = "gpt-4o-mini"
```

5. Despliega la aplicación

## Personalización

### Modificar Acertijos

Edita el archivo `clues.yaml` para cambiar las preguntas, respuestas y pistas:

```yaml
total_questions: 4
questions:
  - id: 1
    question: "¿Tu pregunta aquí?"
    answer: "La respuesta"
    clues:
      - "Primera pista"
      - "Segunda pista"
      - "Tercera pista"
  # ... más preguntas
```

### Personalizar la Interfaz

La aplicación utiliza CSS personalizado que puedes modificar en la sección correspondiente del archivo `app.py`.

## Características Técnicas

- **Streaming de respuestas**: Las respuestas del modelo se muestran gradualmente, simulando una conversación real.
- **Persistencia de datos**: El progreso se guarda en un archivo YAML para mantener el estado entre sesiones.
- **Diseño responsivo**: La interfaz se adapta a diferentes tamaños de pantalla.
- **Agentes LLM**: Dos agentes LLM (AnswerGrader y ClueAssistant) con diferentes personalidades y roles.

## Solución de problemas

- **Error de conexión a Azure OpenAI**: Verifica que tus credenciales sean correctas y que tengas acceso al modelo gpt-4o-mini.
- **Problemas con el archivo de progreso**: Si la aplicación no carga correctamente, puede ser necesario reiniciar el progreso eliminando el archivo `progress.yaml`.

## Licencia

[MIT](LICENSE)

---

Creado con ❤️ para una experiencia de cumpleaños memorable.

