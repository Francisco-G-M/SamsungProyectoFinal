# ⚽ FUTBOLBOT IA: Tu Asistente Inteligente de Fútbol
FUTBOLBOT IA es un proyecto de Capstone que busca ser un asistente futbolero inteligente diseñado para el hincha. Nuestro objetivo es entender emociones, responder consultas sobre equipos locales, analizar audios e imágenes, y acercar la tecnología de IA al fanático del fútbol argentino de una manera natural y divertida.

# 🧠 Características Principales
Este bot combina múltiples tecnologías de IA para crear una experiencia de usuario integral:

Procesamiento de Lenguaje Natural (PLN): Implementado para un análisis de sentimientos avanzado en español.

Reconocimiento de Voz: Permite una interacción fluida al convertir los audios de los usuarios en texto procesable.

Análisis de Imágenes: Capacidad de analizar las imágenes enviadas por el usuario.

Base de Conocimiento: El bot responde consultas basándose en un dataset curado de 15,000 preguntas y respuestas.

Interacción Natural: Las respuestas están diseñadas para ser cortas, directas y fluidas, simulando una conversación real.

🚀 Instalación y Puesta en Marcha
Requisito Previo: Este proyecto fue desarrollado y probado con Python 3.10.11. Los siguientes pasos asumen que estás usando una terminal Git Bash en Windows.

# Clonar el Repositorio
Primero, clona el proyecto en tu máquina local y navega al directorio.

Bash

 Remplaza [URL-DEL-REPOSITORIO] con la URL de tu proyecto
  git clone [URL-DEL-REPOSITORIO]
  cd SamsungProyectoFinal/
# Configurar el Entorno Virtual
Es una buena práctica usar un entorno virtual para manejar las dependencias del proyecto.En Bash es:

# 1. Crear el entorno virtual
python -m venv entorno-virtual

# 2. Activar el entorno virtual (específico para Git Bash)
  source entorno-virtual/Scripts/activate
Tu terminal ahora debería mostrar (entorno-virtual) al principio de la línea.

# 3. Instalar Dependencias
Una vez activado el entorno, instala todas las librerías necesarias.En Bash es:
  pip install -r requirements.txt

# 4. Configurar las Claves API
El bot necesita claves API para conectarse a los servicios de Telegram y Groq.
En la carpeta raíz del proyecto (SamsungProyectoFinal), crea un archivo llamado .env.
Abre el archivo .env y añade tus claves de la siguiente manera:

  TELEGRAM_BOT_TOKEN="AQUÍ_VA_TU_TOKEN_DE_TELEGRAM"
  GROQ_API_KEY="AQUÍ_VA_TU_CLAVE_DE_GROQ"

# 5. Ejecutar el Proyecto
Con el entorno activado y las claves configuradas, ya puedes ejecutar el bot.En Bash es:
  python mainProyecto.py

# 🤖 Comandos de Telegram
/start Inicia la conversación con el bot. Muestra un mensaje de bienvenida y una lista de todos los comandos disponibles.

/help Muestra la lista completa de comandos que puedes usar.

/faq El bot seleccionará una pregunta y respuesta aleatoria de su base de datos y te la mostrará.

/transmision Muestra un mensaje con canales recomendados para ver la mayoría de los partidos.

/analizar [texto o imagen] Este comando tiene dos usos:

Con texto: Envía el comando seguido de un mensaje (ej: /analizar ¡Qué gran partido!). El bot devolverá el sentimiento principal (ej: Positivo) y su porcentaje.

Con una imagen: Envía una imagen y usa /analizar en el pie de foto (o simplemente envía la imagen). El bot devolverá un análisis de la misma.

# 📈 Impacto Potencial y Escalabilidad
El diseño del proyecto está pensado para la expansión y la integración con sistemas externos.

Adaptabilidad: El bot puede ampliarse fácilmente para cubrir más clubes, ligas o incluso la selección nacional.

Integración en Tiempo Real: La arquitectura permite una futura integración con APIs de resultados en tiempo real para dar información actualizada al minuto.

Expansión Regional: El modelo tiene potencial para adaptarse a otros deportes o regiones, simplemente ajustando el tono y la base de datos.
