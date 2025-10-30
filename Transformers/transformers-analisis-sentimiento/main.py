import os
import telebot
from transformers import pipeline
import time # Mantén esta importación si quieres usar sleep en otros lugares

# Configuración del bot
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7636746872:AAG_1EgeTtR7K3_mCyYqwgNrXMHuo4Q7hw0")
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Carga del modelo de análisis de sentimiento
print("Cargando el modelo de análisis de sentimiento...")
analizador_de_sentimiento = pipeline(
    "sentiment-analysis",
    model="pysentimiento/robertuito-sentiment-analysis"
)
print("Modelo cargado con exitosichion")

# Función para analizar el sentimiento y devolver el texto con emojis
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

# Manejador para los comandos /start y /help
@bot.message_handler(commands=['start', 'help'])
def cmd_welcome(message):
    bot.send_chat_action(message.chat.id, "typing")
    # Elimina time.sleep(10) para una respuesta más rápida
    bot.reply_to(message, "¡Bienvenido! Dame una frase y analizo el sentimiento.")

# Manejador para cualquier mensaje de texto que no sea un comando
@bot.message_handler(func=lambda message: True)
def analizar_mensaje(message):
    texto = message.text
    resultado = analizar_sentimiento(texto)
    bot.reply_to(message, resultado)

if __name__ == "__main__":
    print("Bot ejecutado")
    # Inicia el bot para que escuche mensajes indefinidamente
    bot.infinity_polling()