import base64
from bot_setup import cliente_groq, analizador_de_sentimiento

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