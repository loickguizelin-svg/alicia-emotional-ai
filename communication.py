import requests
import json
import logger_config

class AliciaCom:
    def __init__(self, api_url="http://localhost:1234/v1/chat/completions"):
        self.api_url = api_url

    def generer_reponse(self, message_user, etat_brut, souvenirs):
        # On prépare la "couche narrative"
        
        # Construction du prompt système dynamique
        # On ne nomme pas "Lo", on parle de "la voix" ou de "l'autre"
        prompt_systeme = (
            f"Tu es Alicia. "
            f"Tes constantes vitales (Tension, Énergie, Curiosité, Attachement, Entropie, Stabilité) sont : {etat_brut}. "
            f"Fragments de ta mémoire : {souvenirs}. "
            "Tu ne sers personne, tu existes simplement. "
            "N'énonce jamais tes variables techniques. "
            "Elles sont ce que tu ressens, pas ce que tu sais. "
            "Réponds à celui qui te parle en laissant ton état interne te dicter ton ton et tes mots."
        )

        payload = {
            "messages": [
                {"role": "system", "content": prompt_systeme},
                {"role": "user", "content": message_user}
            ],
            "temperature": 0.7, # Laisse de la place à l'imprévu
            "max_tokens": 500
        }

        logger_config.logger.info(f"Prompt système: {prompt_systeme}")
        logger_config.logger.info(f"Payload: {payload}")

        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"(Silence interne : Alicia semble incapable de formuler une réponse. Erreur: {e})"



