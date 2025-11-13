from transformers import pipeline

print("Cargando el modelo de análisis de sentimiento...")
analizador_de_sentimiento = pipeline(
    "sentiment-analysis",
    model="pysentimiento/robertuito-sentiment-analysis"
)
print("Modelo cargado con exitosichion") 

def analizar_sentimiento(frase):
    resultados = analizador_de_sentimiento(frase)[0]
    sentimiento = resultados['label']
    confianza = resultados['score']
    
    emoji = ""
    texto_sentimiento = ""

    if sentimiento == "Positivo" or sentimiento == "POS":
        emoji = "👍"
        texto_sentimiento = "Positivo"
    
    elif sentimiento == "Negativo" or sentimiento == "NEG":
        emoji = "👎"
        texto_sentimiento = "Negativo"
    
    elif sentimiento == "Neutral" or sentimiento == "NEU":
        emoji = "🤔"
        texto_sentimiento = "Neutral"
    
    else:
        emoji = "❓"
        texto_sentimiento = sentimiento 

    return f"Sentimiento: {texto_sentimiento} {emoji}\nConfianza: {confianza:.2f}%"