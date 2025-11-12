# Este es tu nuevo archivo (ej: Transformers/analisis_sentimiento/core.py)
# Se eliminó todo el código de 'telebot', 'os' y los handlers.

from transformers import pipeline

# 1. Carga el modelo aquí
print("Cargando el modelo de análisis de sentimiento...")
analizador_de_sentimiento = pipeline(
    "sentiment-analysis",
    model="pysentimiento/robertuito-sentiment-analysis"
)
# (Opcional: puedes corregir esta errata a "con éxito")
print("Modelo cargado con exitosichion") 

# 2. Define la función aquí
def analizar_sentimiento(frase):
    resultados = analizador_de_sentimiento(frase)[0]
    sentimiento = resultados['label']
    confianza = resultados['score']
    
    emoji = ""
    texto_sentimiento = ""

    # Comprobamos si la etiqueta es 'POS' O 'Positivo'
    if sentimiento == "Positivo" or sentimiento == "POS":
        emoji = "👍"
        texto_sentimiento = "Positivo"
    
    # Comprobamos si la etiqueta es 'NEG' O 'Negativo'
    elif sentimiento == "Negativo" or sentimiento == "NEG":
        emoji = "👎"
        texto_sentimiento = "Negativo"
    
    # Comprobamos si la etiqueta es 'NEU' O 'Neutral'
    elif sentimiento == "Neutral" or sentimiento == "NEU":
        emoji = "🤔"
        texto_sentimiento = "Neutral"
    
    # Por si devuelve algo inesperado
    else:
        emoji = "❓"
        texto_sentimiento = sentimiento 

    # Usamos la variable 'texto_sentimiento' para mostrar siempre la palabra completa
    return f"Sentimiento: {texto_sentimiento} {emoji}\nConfianza: {confianza:.2f}%"

# Se eliminó todo el código de bot.message_handler 
# y el if __name__ == "__main__"