import json
import random

class FaqManager:
    """
    Gestiona la carga y el acceso a las preguntas frecuentes
    sobre fútbol argentino desde un archivo JSON.
    """
    def __init__(self, file_path='dataset.json'):
        self.file_path = file_path
        self.faq_data = self._load_data()

    def _load_data(self):
        """
        Carga los datos del archivo JSON. Maneja dos estructuras:
        1. Un diccionario con la clave "preguntas_frecuentes_futbol_argentino".
        2. Una lista directa (si el JSON comienza con '[').
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # --- LÓGICA DE DETECCIÓN Y EXTRACCIÓN MODIFICADA ---
            if isinstance(data, list):
                # Si el JSON es una lista directa
                faq_list = data
            elif isinstance(data, dict):
                # Si el JSON es un diccionario con la clave esperada
                faq_list = data.get("preguntas_frecuentes_futbol_argentino", [])
            else:
                # Si no es ni lista ni diccionario
                faq_list = []
                
            print(f"✅ FaqManager: Dataset cargado con {len(faq_list)} preguntas.")
            return faq_list
            
        except FileNotFoundError:
            print(f"❌ ERROR: FaqManager no pudo encontrar el archivo '{self.file_path}'.")
            return []
        except json.JSONDecodeError:
            print(f"❌ ERROR: El archivo '{self.file_path}' tiene un formato JSON inválido.")
            return []

    def get_random_faq(self):
        """
        Devuelve una pregunta y respuesta aleatoria, adaptando las claves 
        ('question', 'answer') a las claves esperadas por el main.py ('pregunta', 'respuesta')
        y asignando 'General' si la categoría falta.
        """
        if not self.faq_data:
            return None
        
        pregunta_original = random.choice(self.faq_data)
        
        # Adaptamos y estandarizamos las claves:
        return {
            # Asignamos 'General' si la clave 'categoria' falta
            "categoria": pregunta_original.get('categoria', 'General'), 
            # Adaptamos de 'question' a 'pregunta', usando un fallback robusto
            "pregunta": pregunta_original.get('question', pregunta_original.get('pregunta', 'Error: Clave de pregunta faltante.')),
            # Adaptamos de 'answer' a 'respuesta', usando un fallback robusto
            "respuesta": pregunta_original.get('answer', pregunta_original.get('respuesta', 'Error: Clave de respuesta faltante.'))
        }

    def get_transmision_info(self):
        """Devuelve la información estática sobre los canales de transmisión."""
        info = (
            "**📺 Canales de Transmisión del Fútbol Argentino**\n\n"
            "Para ver la mayoría de los partidos de la **Liga Profesional de Fútbol (Primera División)** "
            "es necesario contratar el **Pack Fútbol**.\n\n"
            "Los canales principales son:\n"
            "* **ESPN Premium**\n"
            "* **TNT Sports**\n\n"
            "Otros torneos:\n"
            "* **Copa Argentina:** TyC Sports\n"
            "* **Primera Nacional:** TyC Sports / DirecTV Sports / DeporTV\n\n"
            "Recuerda que estas señales son premium y requieren una suscripción adicional."
        )
        return info
    
    def buscar_respuesta(self, texto_usuario):
        """
        Busca una respuesta en el dataset comparando el texto del usuario
        con las preguntas del archivo JSON. Devuelve la respuesta si encuentra coincidencia.
        """
        texto_usuario = texto_usuario.lower()

        for item in self.faq_data:
            # Soporta tanto claves 'pregunta' como 'question'
            pregunta = item.get('pregunta') or item.get('question')
            respuesta = item.get('respuesta') or item.get('answer')

            if pregunta and respuesta:
                # Coincidencia simple: si la pregunta del dataset está dentro del texto del usuario
                if pregunta.lower() in texto_usuario:
                    return respuesta

        return None
    