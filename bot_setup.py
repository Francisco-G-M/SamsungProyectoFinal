import os
import telebot
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CLAVE_API_GROQ = os.getenv('GROQ_API_KEY')

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN no está configurado. Revisa tu archivo .env")

if not CLAVE_API_GROQ:
    raise ValueError("GROQ_API_KEY no está configurado. Revisa tu archivo .env")

print("🤖 Iniciando bot de Telegram...")
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

print("🤖 Conectando con Groq...")
cliente_groq = Groq(api_key=CLAVE_API_GROQ)