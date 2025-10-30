import os
import telebot
from transformers import pipeline
import base64
from groq import Groq
from dotenv import load_dotenv
import io
import requests

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CLAVE_API_GROQ = os.getenv('GROQ_API_KEY')

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN no está configurado. Revisa tu archivo .env")

if not CLAVE_API_GROQ:
    raise ValueError("GROQ_API_KEY no está configurado. Revisa tu archivo .env")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
cliente_groq = Groq(api_key=CLAVE_API_GROQ)

print("Cargando el modelo de análisis de sentimiento...")
analizador_de_sentimiento = pipeline(
    "sentiment-analysis",
    model="pysentimiento/robertuito-sentiment-analysis"
)
print("Modelo de sentimiento cargado con éxito.")

def analizar_sentimiento(frase):
    resultados = analizador_de_sentimiento(frase)[0]
    sentimiento = resultados['label']
    confianza = resultados['score']
    
    emoji = ""
    if sentimiento == "POS":
        emoji = "👍"
    elif sentimiento == "NEG":
        emoji = "👎"
    elif sentimiento == "NEU":
        emoji = "🤔"
        
    return f"Sentimiento: {sentimiento} {emoji}\nConfianza: {confianza:.2f}%"

def imagen_a_base64(ruta_o_bytes_imagen):
    try:
        if isinstance(ruta_o_bytes_imagen, bytes):
            return base64.b64encode(ruta_o_bytes_imagen).decode('utf-8')
        
        else:
            with open(ruta_o_bytes_imagen, "rb") as archivo_imagen:
                return base64.b64encode(archivo_imagen.read()).decode('utf-8')
    
    except Exception as e:
        print(f"Error al convertir imagen a base64: {e}")
        return None

def describir_imagen_con_groq(imagen_base64):
    try:
        completado_chat = cliente_groq.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Por favor, describe esta imagen de manera detallada y clara en español."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{imagen_base64}"
                            }
                        }
                    ]
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.7,
            max_tokens=1000
        )
        return completado_chat.choices[0].message.content
        
    except Exception as e:
        print(f"Error al describir imagen con Groq: {e}")
        return None

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
    print("🤖 Bot multifunción ejecutado (Sentimientos + Imágenes)")
    print("📸 Esperando mensajes o imágenes...")
    
    try:
        bot.infinity_polling()
    
    except Exception as e:
        print(f"Error al iniciar el bot: {e}")