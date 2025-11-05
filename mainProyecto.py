import telebot
from bot_setup import bot
from bot_dataset import FaqManager
from bot_functions import (
    analizar_sentimiento, 
    imagen_a_base64, 
    describir_imagen_con_groq
)

faq_manager = FaqManager()

@bot.message_handler(commands=['start', 'help'])
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
def random_faq(message):
    bot.send_chat_action(message.chat.id, 'typing')

    pregunta_aleatoria = faq_manager.get_random_faq()
    
    if pregunta_aleatoria:
        categoria = pregunta_aleatoria['categoria']
        pregunta = pregunta_aleatoria['pregunta']
        respuesta = pregunta_aleatoria['respuesta']
        
        if "Error: Clave" in pregunta or "Error: Clave" in respuesta:
             bot.reply_to(message, "❌ Disculpa, el formato de la pregunta seleccionada es irrecuperable. Intenta de nuevo o revisa tu dataset.json.")
             return

        respuesta_faq = (
            f"PREGUNTA (Categoría: {categoria})\n"
            f"{pregunta}\n\n"
            f"RESPUESTA\n"
            f"{respuesta}"
        )
        
        bot.reply_to(message, respuesta_faq)
    
    else:
        bot.reply_to(message, "Disculpa, el banco de preguntas de fútbol no está disponible. Revisa si dataset.json existe y es válido.")

@bot.message_handler(commands=['transmision'])
def info_transmision(message):
    bot.send_chat_action(message.chat.id, 'typing')
    
    info = faq_manager.get_transmision_info()
    
    bot.reply_to(message, info)

@bot.message_handler(commands=['analizar'])
def cmd_analizar_sentimiento(message):
    """
    Analiza el sentimiento del texto que sigue al comando /analizar.
    """
    try:
        texto_a_analizar = message.text.split(maxsplit=1)[1]
    
    except IndexError:
        texto_ayuda = "Por favor, escribe el texto que quieres analizar después del comando.\n\n"
        texto_ayuda += "Ejemplo: /analizar ¡Qué buen servicio!"
        bot.reply_to(message, texto_ayuda)
        return

    bot.send_chat_action(message.chat.id, 'typing')
    resultado = analizar_sentimiento(texto_a_analizar)
    bot.reply_to(message, resultado)

@bot.message_handler(content_types=['photo'])
def responder_foto(message):
    
    bot.reply_to(message, "📸 He recibido tu imagen. Analizándola... ⏳")
    
    try:
        foto = message.photo[-1]
        
        info_archivo = bot.get_file(foto.file_id)
        archivo_descargado = bot.download_file(info_archivo.file_path)
        
        imagen_base64 = imagen_a_base64(archivo_descargado)
        
        if not imagen_base64:
            bot.reply_to(message, "❌ Error al procesar la imagen. Intenta de nuevo.")
            return
            
        descripcion = describir_imagen_con_groq(imagen_base64)
        
        if descripcion:
            respuesta = f"Descripción de la imagen:\n\n{descripcion}"
            bot.reply_to(message, respuesta)
        else:
            bot.reply_to(message, "❌ No pude analizar la imagen. Por favor, intenta con otra imagen.")
            
    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        bot.reply_to(message, "❌ Ocurrió un error al procesar tu imagen. Intenta de nuevo.")

@bot.message_handler(content_types=['text'])
def responder_preguntas_dataset(message):
    
    if message.text.startswith('/'):
        bot.reply_to(message, "🤔 Comando no reconocido. Escribe /start para ver la lista de comandos.")
        return 

    bot.send_chat_action(message.chat.id, 'typing')
    
    resultado = faq_manager.buscar_respuesta(message.text)
    
    if resultado:
        categoria = resultado.get('categoria', 'General')
        pregunta = resultado.get('pregunta', 'N/A')
        respuesta = resultado.get('respuesta', 'N/A')
        
        if "Error: Clave" in pregunta or "Error: Clave" in respuesta:
             bot.reply_to(message, "❌ Disculpa, encontré la pregunta pero su formato es irrecuperable. Revisa tu dataset.json.")
             return

        respuesta_faq = (
            f"PREGUNTA (Categoría: {categoria})\n"
            f"{pregunta}\n\n"
            f"RESPUESTA\n"
            f"{respuesta}"
        )
        bot.reply_to(message, respuesta_faq)
        
    else:
        texto_ayuda = (
            "🤔 Mmm, no encontré una respuesta exacta para eso en mi base de datos de fútbol.\n\n"
            "Recuerda que puedes usar:\n"
            "/faq - Pregunta aleatoria.\n"
            "/transmision - Info de partidos.\n"
            "/analizar [tu texto] - Analizo el sentimiento.\n\n"
            "O puedes enviarme una foto."
        )
        bot.reply_to(message, texto_ayuda)


if __name__ == "__main__":
    print("Bot en funcionamiento...")
    print("(Manejo de señales, imágenes, comandos y búsqueda en dataset...)")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Error al iniciar el bot: {e}")