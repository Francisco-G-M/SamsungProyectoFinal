⚽ FUTBOLBOT IA: Tu Asistente Inteligente de Fútbol

"""
## 🚀 Instalación (Usando Git Bash)

Este proyecto fue desarrollado y probado con **Python 3.10.11**. Los siguientes pasos asumen que estás usando una terminal **Git Bash** en Windows.
--Clonar el Repositorio:

Primero debes clonar el proyecto en tu máquina:

```bash
# Reemplaza [URL-DEL-REPOSITORIO] con la URL de tu proyecto
git clone [URL-DEL-REPOSITORIO]
cd SamsungProyectoFinal/

--Configurar el Entorno Virtual:
Para que el proyecto funcione, necesitas crear un entorno virtual e instalar las dependencias.

1-Crear un entorno virtual: (Se recomienda crearlo con el nombre emtorno-virtual en la raíz del proyecto)
  python -m venv entorno-virtual

2-Activar el entorno virtual: (Este es el comando específico para Git Bash).
  source entorno-virtual/Scripts/activate
Para saber si esta activado tu terminal ahora debería mostrar (entorno-virtual) al principio.

3-Instalar Dependencias:
Una vez activado el entorno, instala todas las librerías necesarias ejecutando:
  pip install -r requirements.txt

4-Configurar las claves API:
Este proyecto necesita claves API para funcionar, las cuales se guardan en un archivo .env en la raíz del proyecto
 4a-En la carpeta raíz (SamsungProyectoFinal), crea un archivo llamado .env
 4b-Ábrelo y añade tus claves (reemplaza los valores de ejemplo):
    TELEGRAM_BOT_TOKEN="AQUÍ_VA_TU_TOKEN_DE_TELEGRAM"
    GROQ_API_KEY="AQUÍ_VA_TU_CLAVE_DE_GROQ"

5-Ejecutar el proyecto:
Con el entorno activado (entorno-virtual) y las dependencias instaladas, puedes ejecutar el bot:
   python mainProyecto.py
"""

1) Propósito del chatbot
FUTBOLBOT IA es un proyecto de Capstone que busca ser un asistente futbolero inteligente diseñado para el hincha. Nuestro objetivo es entender emociones, 
responder consultas sobre equipos locales, analizar audios e imágenes, 
y acercar la tecnología de IA al fanático del fútbol argentino de una manera natural y divertida.

2) Funcionalidad y Experiencia de Uso
Enfoque: Lograr una interacción natural y fluida.

Diseño de Conversación Fluida: Acepta comandos claros a través de voz, imagen y texto/sentimiento.

Interacción Natural: El bot contesta con mensajes cortos y directos.

3) Aplicación de Inteligencia Artificial

Enfoque: Combinar múltiples tecnologías de IA para una experiencia integral.

Los tres pilares de IA en FUTBOLBOT son:

Procesamiento de Lenguaje Natural (PLN): Implementado para el análisis de sentimientos en español.

Reconocimiento de Voz: Permite la interacción convirtiendo los audios de los usuarios en texto.

Análisis de Emociones: Una función clave para analizar las emociones del usuario.

Capacidad de respuesta: El bot responde en base a un dataset de 15mil preguntas. 

4) Comandos del chatBot en Telegram:


/start -> Este comando se utiliza para iniciar el chat del bot. 
Aparecera un mensaje de presentación con todos los comandos que el usuario de Telegram puede utilizar en el chat, los cuales son.

/help -> Este comando muestra una lista con todos los comandos disponibles del bot, los cuales son:

 /faq -> Este comando se utiliza para que el bot tome un par pregunta y respuesta aleatoria de su dataset, y se lo muestre al usuario vía chat.

 /transmision -> Este comando se utiliza para que el bot muestre una mensaje de canales recomendados para ver la mayoría de los partidos.

 /analizar -> Este comando se utiliza junto con un mensaje, e.j: /analizar Buenos Dias. 
 El bot devolvera un mensaje indicanco el sentimiento principal del mensaje junto con el porcentaje del mismo presente en el mensaje. 
 E.j: /analizar Buenos Dias devuelve un sentimiento Neutral y un porcentaje de 0.52%

 En el caso de que se le pase una imagen, el bot devolvera un analisis de la imagen proporcionada.

5) Creatividad e Innovación

Punto Clave: Combina tres tipos de IA (texto, voz, imagen) en un solo bot.

Integrar las capacidades de IA para texto, voz e imagen en una única experiencia.

Su capacidad para analizar y responder a las emociones del usuario.

6) Impacto Potencial y Escalabilidad

Enfoque: Diseño pensado para la expansión y la integración con sistemas externos.

Adaptabilidad: Puede ampliarse a distintos clubes o selecciones más allá del enfoque local inicial.

Integración en Tiempo Real: Permite la integración con APIs de resultados en tiempo real para información actualizada.

Expansión Regional: Tiene potencial para adaptarse a otros deportes o regiones, simplemente ajustando el tono y la base de datos (dataset).
