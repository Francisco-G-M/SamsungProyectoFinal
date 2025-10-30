from bot_setup import bot 

from bot_functions import (
    analizar_sentimiento, 
    imagen_a_base64, 
    describir_imagen_con_groq
)

@bot.message_handler(commands=['start', 'help'])
def cmd_welcome(message):
    texto_bienvenida = """
¡Hola! 👋 Soy un bot multifunción.

🤖 **¿Qué puedo hacer?**

1.  **Analizar Sentimientos:** Envíame un mensaje de texto y te diré si es positivo, negativo o neutral.
2.  **Describir Imágenes:** Envíame una imagen y te daré una descripción detallada.

¡Pruébame!
    """
    bot.reply_to(message, texto_bienvenida)

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
    print("📸 Esperando mensajes o imágenes...")
    
    try:
        bot.polling(none_stop=True) 
    
    except Exception as e:
        print(f"Error al iniciar el bot: {e}")