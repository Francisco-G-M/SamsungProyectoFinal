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
        self.transmision_info = self._get_transmision_info_internal()

    def _load_data(self):
        """
        Carga los datos del archivo JSON. Maneja dos estructuras:
        1. Un diccionario con la clave 'preguntas_futbol_argentino'.
        2. Una lista directa de preguntas.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, dict):
                faq_list = data.get("preguntas_futbol_argentino", [])
            elif isinstance(data, list):
                faq_list = data
            else:
                faq_list = []

            print(f"✅ FaqManager: Dataset cargado con {len(faq_list)} preguntas.")
            return faq_list

        except FileNotFoundError:
            print(f"❌ ERROR: FaqManager no pudo encontrar el archivo {self.file_path}")
            return []
        except json.JSONDecodeError:
            print(f"❌ ERROR: El archivo {self.file_path} tiene un formato JSON inválido.")
            return []

    def get_random_faq(self):
        """
        Devuelve una pregunta y respuesta aleatoria, adaptando las claves.
        """
        if not self.faq_data:
            return None 
        
        pregunta_original = random.choice(self.faq_data)
        
        pregunta_adaptada = {
            'categoria': pregunta_original.get('categoria', 'General'),
            'pregunta': pregunta_original.get('pregunta', pregunta_original.get('question', 'Error: Clave de pregunta faltante.')),
            'respuesta': pregunta_original.get('respuesta', pregunta_original.get('answer', 'Error: Clave de respuesta faltante.'))
        }
        return pregunta_adaptada

    def _get_transmision_info_internal(self):
        """
        Genera el texto estático sobre los canales de transmisión.
        """
        info = (
            "📺 Info de Transmisión del Fútbol Argentino\n\n"
            "Para ver la mayoría de los partidos de la Liga Profesional de Fútbol (Primera División), "
            "se necesita contratar el 'Pack Fútbol'.\n\n"
            "Los canales principales son:\n"
            "🔸 ESPN Premium\n"
            "🔸 TNT Sports\n\n"
            "Otros torneos:\n"
            "🔹 Copa Argentina: TyC Sports\n"
            "🔹 Primera Nacional: TyC Sports / DirecTV Sports\n\n"
            "*(Recuerda que estas señales son premium y requieren una suscripción adicional.)*"
        )
        return info

    def get_transmision_info(self):
        return self.transmision_info

    # --- FUNCIÓN DE NORMALIZACIÓN AÑADIDA ---
    def _normalizar_texto(self, texto):
        """
        Quita tildes, puntuación básica y pasa a minúsculas.
        """
        if not isinstance(texto, str):
            return ""
            
        texto = texto.lower()
        # Quitar tildes
        texto = texto.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
        # Quitar puntuación básica
        texto = texto.replace('?', '').replace('¿', '').replace('.', '').replace(',', '').replace('!', '').replace('¡', '')
        return texto.strip()

    # --- FUNCIÓN DE BÚSQUEDA CORREGIDA Y MEJORADA ---
    def buscar_respuesta(self, texto_usuario):
        """
        Busca una respuesta en el dataset basada en el texto del usuario.
        """
        if not self.faq_data:
            return None # No hay datos cargados

        # 1. Normalizamos la entrada del usuario
        texto_usuario_normalizado = self._normalizar_texto(texto_usuario)
        if not texto_usuario_normalizado:
            return None # Usuario no escribió nada útil

        for item in self.faq_data:
            
            # 2. Obtenemos la pregunta (¡CORREGIDO!)
            #    Buscamos 'pregunta' O 'question'
            texto_pregunta_original = item.get('pregunta', item.get('question', ''))
            
            # 3. Normalizamos la pregunta del dataset
            texto_pregunta_normalizado = self._normalizar_texto(texto_pregunta_original)
            
            if not texto_pregunta_normalizado:
                continue # Saltar si la pregunta en el JSON está vacía

            # 4. LÓGICA DE BÚSQUEDA MEJORADA
            #    Comparamos si la pregunta del dataset (ej: "que colores usa union")
            #    está contenida en el texto del usuario (ej: "me decis que colores usa union")
            #    o si son idénticas.
            if texto_pregunta_normalizado in texto_usuario_normalizado:
                
                # ¡Encontramos una coincidencia!
                # Adaptamos las claves para asegurarnos de que el formato de retorno sea correcto
                pregunta_adaptada = {
                    'categoria': item.get('categoria', 'General'),
                    'pregunta': item.get('pregunta', item.get('question', 'N/A')),
                    'respuesta': item.get('respuesta', item.get('answer', 'N/A'))
                }
                return pregunta_adaptada
        
        # Si termina el bucle y no encuentra nada, devuelve None
        return None