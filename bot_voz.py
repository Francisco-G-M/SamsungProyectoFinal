import telebot as tlb
import os
import json
from groq import Groq
from typing import Optional
import time
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("No se encuentra el TOKEN de Telegram en .env")
if not GROQ_API_KEY:
    raise ValueError("No se encuentra el API_KEY de Groq en .env")

# Instanciar bot y cliente Groq
bot = tlb.TeleBot(TELEGRAM_BOT_TOKEN)
groq_client = Groq(api_key=GROQ_API_KEY)

# Cargar dataset local
def load_futbol_data():
    try:
        with open("futbol_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error al cargar JSON: {e}")
        return None

futbol_data = load_futbol_data()

# Obtener respuesta con IA Groq
def get_groq_response(user_message: str) -> Optional[str]:
    try:
        system_prompt = f"""
Sos un asistente virtual futbolero argentino 🇦🇷 llamado FutbolBot ⚽🔥.
Respondé con tono pasional, amistoso y natural sobre fútbol.

Usá la siguiente info como base:
{json.dumps(futbol_data, ensure_ascii=False, indent=2)}

Reglas:
1. Usá info del dataset si existe.
2. No inventes datos falsos.
3. Si no sabés, decilo con naturalidad.
4. Usá emojis de fútbol ⚽🏆🔥.
5. Evitá favoritismos fuertes.
6. No saludes más de una vez.
"""

        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.5,
            max_tokens=500
        )

        return chat_completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error: {str(e)}")
        return None

# Transcribir audio con Whisper
def transcribe_voice_with_groq(message: tlb.types.Message) -> Optional[str]:
    try:
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        temp_file = "temp_voice.ogg"

        with open(temp_file, "wb") as f:
            f.write(downloaded_file)

        with open(temp_file, "rb") as file:
            transcription = groq_client.audio.transcriptions.create(
                file=(temp_file, file.read()),
                model="whisper-large-v3-turbo",
                prompt="Transcripción futbolera en español",
                response_format="json",
                language="es",
                temperature=1
            )

        os.remove(temp_file)
        return transcription.text

    except Exception as e:
        print(f"Error al transcribir: {str(e)}")
        return None

# /start
@bot.message_handler(commands=['start'])
def send_welcome(message: tlb.types.Message):
    if not futbol_data:
        bot.reply_to(message, "⚠️ Error al cargar datos de fútbol.")
        return

    welcome_prompt = "Creá un mensaje de bienvenida futbolero que invite a hablar de fútbol argentino."
    response = get_groq_response(welcome_prompt)
    bot.reply_to(message, response or "Error al generar bienvenida.")

# Mensajes de texto
@bot.message_handler(content_types=['text'])
def handle_text_message(message: tlb.types.Message):
    if not futbol_data:
        bot.reply_to(message, "⚠️ Error al cargar datos de fútbol.")
        return

    bot.send_chat_action(message.chat.id, 'typing')
    response = get_groq_response(message.text)
    bot.reply_to(message, response or "❌ No pude procesar tu mensaje ⚽")

# Mensajes de voz
@bot.message_handler(content_types=['voice'])
def handle_voice_message(message: tlb.types.Message):
    if not futbol_data:
        bot.reply_to(message, "⚠️ Error al cargar datos de fútbol.")
        return

    bot.send_chat_action(message.chat.id, 'typing')
    transcription = transcribe_voice_with_groq(message)
    if not transcription:
        bot.reply_to(message, "🎙️ No pude entender el audio, probá de nuevo 😉")
        return

    response = get_groq_response(transcription)
    bot.reply_to(message, response or "❌ Error al responder ⚽")

# Iniciar bot
if __name__ == "__main__":
    if futbol_data:
        print("🤖 FutbolBot iniciado con Groq y Whisper 🎙️⚽")
        while True:
            try:
                bot.polling(none_stop=True, interval=0, timeout=20)
            except Exception as e:
                print(f"Error en el bot: {str(e)}")
                print("Reiniciando en 5 segundos...")
                time.sleep(3)
    else:
        print("Error: no se pudo cargar el archivo JSON.")

