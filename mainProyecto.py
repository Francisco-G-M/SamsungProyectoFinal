from bot_setup import bot, analizador_de_sentimiento, cliente_groq 
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