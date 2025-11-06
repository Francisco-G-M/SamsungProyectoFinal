from bot_setup import bot, analizador_de_sentimiento, cliente_groq, get_groq_response
from bot_dataset import FaqManager 
from bot_functions import (
    analizar_sentimiento, 
    imagen_a_base64, 
    describir_imagen_con_groq
)
import os
import tempfile

faq_manager = FaqManager() 

@bot.message_handler(commands=['start', 'help'])
def cmd_welcome(message):
    texto_bienvenida = """
¡Hola! 👋 Soy un bot multifunción.

🤖 **¿Qué puedo hacer?**

1.  **Analizar Sentimientos:** Envíame un mensaje de texto y te diré si es positivo, negativo o neutral.
2.  **Describir Imágenes:** Envíame una imagen y te daré una descripción detallada.
3.  **Fútbol Argentino 🇦🇷 (¡Nuevo!):**
    * Usa **/faq** para una pregunta aleatoria de fútbol.
    * Usa **/transmision** para saber dónde ver los partidos.

¡Pruébame!
    """
    bot.reply_to(message, texto_bienvenida, parse_mode='Markdown')

@bot.message_handler(commands=["faq"])
def random_faq(message):
    bot.send_chat_action(message.chat.id, "typing")
    
    pregunta_aleatoria = faq_manager.get_random_faq() 
    
    if pregunta_aleatoria:
        categoria = pregunta_aleatoria['categoria']
        pregunta = pregunta_aleatoria['pregunta']
        respuesta = pregunta_aleatoria['respuesta']
        
        if "Error: Clave" in pregunta or "Error: Clave" in respuesta:
            bot.reply_to(message, "❌ Disculpa, el formato de la pregunta seleccionada es irrecuperable. Intenta de nuevo o revisa tu `dataset.json`.")
            return

        respuesta_faq = (
            f"**❓ PREGUNTA (Categoría: {categoria})**\n"
            f"{pregunta}\n\n"
            f"**✅ RESPUESTA**\n"
            f"{respuesta}"
        )
        
        bot.reply_to(message, respuesta_faq, parse_mode="Markdown")
    else:
        bot.reply_to(message, "Disculpa, el banco de preguntas de fútbol no está disponible. Revisa si `dataset.json` existe y es válido.")

@bot.message_handler(commands=["transmision"])
def info_transmision(message):
    bot.send_chat_action(message.chat.id, "typing")
    
    info = faq_manager.get_transmision_info()
    
    bot.reply_to(message, info, parse_mode="Markdown")

@bot.message_handler(content_types=['photo'])
def manejar_foto(mensaje):
    try:
        bot.reply_to(mensaje, "📸 He recibido tu imagen. Analizándola... ⏳")
        
        foto = mensaje.photo[-1]
        info_archivo = bot.get_file(foto.file_id)
        archivo_descargado = bot.download_file(info_archivo.file_path)
        
        imagen_base64 = imagen_a_base64(archivo_descargado)
        
        if not imagen_base64:
            bot.reply_to(mensaje, "❌ Error al procesar la imagen. Intenta de nuevo.")
            return
        
        descripcion = describir_imagen_con_groq(imagen_base64)
        
        if descripcion:
            respuesta = f"🤖 **Descripción de la imagen:**\n\n{descripcion}"
            bot.reply_to(mensaje, respuesta, parse_mode='Markdown')
        else:
            bot.reply_to(mensaje, "❌ No pude analizar la imagen. Por favor, intenta con otra imagen.")
    
    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        bot.reply_to(mensaje, "❌ Ocurrió un error al procesar tu imagen. Intenta de nuevo.")

@bot.message_handler(content_types=['voice'])
def manejar_voz(message):
    try:
        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, "🎙️ He recibido tu mensaje de voz. Transcribiéndolo... ⏳")

        # Descargar el archivo de voz
        file_info = bot.get_file(message.voice.file_id)
        audio = bot.download_file(file_info.file_path)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as temp_audio:
            temp_audio.write(audio)
            temp_audio_path = temp_audio.name

        # 🔹 Transcripción con Groq Whisper
        with open(temp_audio_path, "rb") as f:
            transcription = cliente_groq.audio.transcriptions.create(
                file=(os.path.basename(temp_audio_path), f.read()),
                model="whisper-large-v3-turbo",
                response_format="text",
                language="es"
            )

        os.remove(temp_audio_path)
        texto_transcrito = transcription.strip()

        if not texto_transcrito:
            bot.reply_to(message, "❌ No pude entender el audio, probá de nuevo 😉")
            return

        # 🔹 Buscar respuesta en dataset (FAQ)
        respuesta_dataset = faq_manager.buscar_respuesta(texto_transcrito) if hasattr(faq_manager, 'buscar_respuesta') else None

        if respuesta_dataset:
            respuesta_final = f"🎯 {respuesta_dataset}"
        else:
            # 🔹 Si no hay respuesta exacta, usar Groq para responder
            respuesta_groq = get_groq_response(texto_transcrito)
            if respuesta_groq:
                respuesta_final = f"🤖 {respuesta_groq}"
            else:
                respuesta_final = "❌ No pude responder a tu pregunta 😅"

        bot.reply_to(message, f"🗣 **Transcripción:**\n_{texto_transcrito}_\n\n{respuesta_final}", parse_mode="Markdown")

    except Exception as e:
        print(f"Error al procesar el audio: {e}")
        bot.reply_to(message, "❌ Ocurrió un error al procesar el mensaje de voz.")


@bot.message_handler(content_types=['text'])
def analizar_mensaje_texto(message):
    if message.text.startswith('/'):
        return
        
    texto = message.text
    resultado = analizar_sentimiento(texto) 
    bot.reply_to(message, resultado)

if __name__ == "__main__":
    print("--- Bot multifunción iniciado ---")
    print("📸 Esperando mensajes, imágenes o comandos de fútbol...")
    
    try:
        bot.polling(none_stop=True) 
    
    except Exception as e:
        print(f"Error al iniciar el bot: {e}")