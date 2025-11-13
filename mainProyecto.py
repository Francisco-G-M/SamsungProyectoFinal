from bot_setup import bot, cliente_groq, get_groq_response
from bot_dataset import faq_manager
from bot_functions import describir_imagen_con_groq
from Transformers.analisis_sentimiento.core import analizar_sentimiento

import telebot
import os
import tempfile

#  Comandos principales

@bot.message_handler(commands=['start'])
def cmd_welcome(message):
    texto_bienvenida = """
¡Hola! 👋
Soy un bot multifunción.

¿Qué puedo hacer?

1. /analizar Sentimiento: Envía un mensaje de texto y te diré si es positivo, negativo o neutral.
    (Debes escribir el comando seguido del texto. Ej: /analizar me encanta esto)
2. Describe Imagen: Envía una imagen y te daré una descripción detallada.
3. Fútbol Argentino 🇦🇷 (¡Nuevo!):
    * Usa /faq para una pregunta aleatoria de fútbol.
    * Usa /transmision para saber dónde ver los partidos.
    * ¡O escríbeme una pregunta (ej: 'cuántas copas tiene boca') e intentaré buscarla en mi base de datos!

¡Pruebame!
"""
    bot.reply_to(message, texto_bienvenida)


@bot.message_handler(commands=['faq'])
def responder_faq(mensaje):
    """
    Muestra las preguntas frecuentes del dataset.
    """
    faqs = faq_manager.obtener_faqs()
    respuesta = "📚 *Preguntas frecuentes:*\n\n"
    for pregunta, respuesta_texto in faqs.items():
        respuesta += f"🔹 *{pregunta}*\n{respuesta_texto}\n\n"
    bot.send_message(mensaje.chat.id, respuesta, parse_mode="Markdown")


@bot.message_handler(commands=['analizar'])
def comando_analizar_sentimiento(mensaje):
    """
    Analiza el sentimiento del texto del usuario.
    """
    texto = mensaje.text.replace("/analizar", "").strip()
    if not texto:
        bot.send_message(mensaje.chat.id, "✍️ Escribí algo después de /analizar para evaluar el sentimiento.")
        return

    resultado = analizar_sentimiento(texto)
    bot.send_message(mensaje.chat.id, f"🧠 Análisis de sentimiento: {resultado}")


@bot.message_handler(commands=['transmision'])
def info_transmision(mensaje):
    """
    Simula información de transmisión de fútbol.
    """
    respuesta = (
        "🎙️ *Transmisión en vivo:* River Plate vs. Boca Juniors\n"
        "🏟️ Estadio Monumental\n"
        "⏰ Domingo 18:00 hs\n"
        "📺 TV Pública / ESPN\n\n"
        "🔥 ¡Viví la pasión del fútbol argentino!"
    )
    bot.send_message(mensaje.chat.id, respuesta, parse_mode="Markdown")

# Handler de mensajes de voz

@bot.message_handler(content_types=['voice'])
def manejar_audio(mensaje):
    """
    Descarga, transcribe y responde mensajes de voz con Groq.
    """
    try:
        archivo_voz = bot.get_file(mensaje.voice.file_id)
        archivo_descargado = bot.download_file(archivo_voz.file_path)

        # Guardar el audio temporalmente
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as temp_audio:
            temp_audio.write(archivo_descargado)
            temp_audio_path = temp_audio.name

        bot.reply_to(mensaje, "🎙️ Procesando tu mensaje de voz, dame un momento...")

        # Transcripción con Groq (Whisper)
        with open(temp_audio_path, "rb") as f:
            transcripcion = cliente_groq.audio.transcriptions.create(
                model="whisper-large-v3",
                file=(os.path.basename(temp_audio_path), f),
                prompt="Transcribí este audio en español de manera natural y clara.",
                response_format="text"
            )

        texto_transcripto = transcripcion.strip()
        print(f"🗣️ Texto transcripto: {texto_transcripto}")

        # Buscar respuesta en dataset
        respuesta_dataset = faq_manager.buscar_respuesta(texto_transcripto)
        if respuesta_dataset:
            bot.send_message(mensaje.chat.id, f"⚽ {respuesta_dataset}")
        else:
            # Si no hay coincidencia, generar respuesta con Groq
            respuesta_groq = get_groq_response(texto_transcripto)
            bot.send_message(mensaje.chat.id, respuesta_groq)

        os.remove(temp_audio_path)

    except Exception as e:
        print(f"Error procesando el audio: {e}")
        bot.reply_to(mensaje, "❌ Ocurrió un error procesando tu mensaje de voz 😅")

# Handler de imágenes

@bot.message_handler(content_types=['photo'])
def manejar_imagen(mensaje):
    """
    Procesa imágenes y devuelve una descripción usando Groq.
    """
    try:
        bot.reply_to(mensaje, "📸 Analizando tu imagen, esperá un momento...")

        # Descargar la foto
        archivo = bot.get_file(mensaje.photo[-1].file_id)
        imagen = bot.download_file(archivo.file_path)

        # Describir con Groq
        from bot_functions import imagen_a_base64
        imagen_base64 = imagen_a_base64(imagen)
        descripcion = describir_imagen_con_groq(imagen_base64)

        bot.send_message(mensaje.chat.id, descripcion)

    except Exception as e:
        print(f"Error procesando imagen: {e}")
        bot.send_message(mensaje.chat.id, "❌ Ocurrió un error al analizar la imagen.")

# Handler de texto general

@bot.message_handler(content_types=['text'])
def manejar_texto(mensaje):
    """
    Responde texto: busca en dataset o genera respuesta con Groq.
    """
    texto = mensaje.text.strip()
    print(f"📩 Mensaje recibido: {texto}")

    # Buscar respuesta en dataset
    respuesta_dataset = faq_manager.buscar_respuesta(texto)
    if respuesta_dataset:
        bot.send_message(mensaje.chat.id, f"⚽ {respuesta_dataset}")
    else:
        # Analizar sentimiento
        sentimiento = analizar_sentimiento(texto)
        print(f"🧠 Sentimiento: {sentimiento}")

        # Respuesta generada por Groq
        respuesta = get_groq_response(texto)
        bot.send_message(mensaje.chat.id, respuesta)

# Iniciar el bot

if __name__ == "__main__":
    print("🤖 Bot Futbolero en ejecución...")
    bot.infinity_polling()
