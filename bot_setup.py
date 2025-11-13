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

print("Cargando el modelo de análisis de sentimiento...")
analizador_de_sentimiento = pipeline(
    "sentiment-analysis",
    model="pysentimiento/robertuito-sentiment-analysis"
)
print("Modelo de sentimiento cargado con éxito.")

def get_groq_response(user_message: str) -> str:
    """
    Envía una consulta a Groq para generar una respuesta basada en el dataset y el mensaje del usuario.
    """
    try:
        system_prompt = """
        Sos un asistente futbolero argentino 🇦🇷 llamado FutbolBot ⚽🔥.
        Respondé con tono pasional, amistoso y natural sobre fútbol.
        Usá la información del dataset si aplica.
        No inventes datos falsos. Si no sabés, decilo con sinceridad.
        Usá emojis futboleros ⚽🏆🔥.
        """

        chat_completion = cliente_groq.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.6,
            max_tokens=400
        )

        return chat_completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error en get_groq_response: {e}")
        return "❌ No pude generar una respuesta en este momento 😅"