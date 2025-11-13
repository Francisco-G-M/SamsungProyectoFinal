import base64
from bot_setup import cliente_groq

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
        # --- ¡PROMPT MEJORADO PARA MÁXIMO DETALLE! ---
        # Le damos un rol dual (experto en fútbol + crítico visual)
        # y una estructura de 4 pasos para forzarlo a ser detallado.
        prompt_experto_detallado = """
        Sos un experto en fútbol argentino 🇦🇷⚽ y un analista visual.
        Tu tarea es describir esta imagen con un nivel de detalle **excepcional y minucioso**.

        Desglosá tu descripción en estos 4 puntos:

        1.  **Contexto General:** ¿Qué es esta imagen? ¿Dónde parece estar tomada? (Ej: un estadio, una cancha, la calle, una captura de pantalla). ¿Qué ambiente se percibe?
        2.  **Sujetos y Acción:** Describe los elementos o personas centrales. ¿Qué están haciendo? ¿Qué ropa llevan? ¿Cómo es su expresión?
        3.  **DETALLE CRÍTICO (FÚTBOL):** PRESTÁ MÁXIMA ATENCIÓN. Si ves un escudo, logo de equipo (Boca, River, etc.), o camiseta de fútbol, identificalo y nombralo CLARAMENTE.
        4.  **Detalles de Fondo y Composición:** Describe los elementos secundarios. Menciona colores predominantes, cualquier texto que sea legible, y otros objetos en el fondo.

        Por favor, sé lo más descriptivo y completo posible en tu respuesta.
        """
        
        completado_chat = cliente_groq.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            # Usamos el nuevo prompt súper detallado
                            "text": prompt_experto_detallado 
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
            model="meta-llama/llama-4-scout-17b-16e-instruct", #
            temperature=0.7, #
            max_tokens=1000 #
        )
        return completado_chat.choices[0].message.content
        
    except Exception as e:
        print(f"Error al describir imagen con Groq: {e}")
        return None