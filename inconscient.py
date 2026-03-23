import chromadb
import logger_config
import random
import time
from datetime import datetime

class AliciaInconscient:
    def __init__(self, affects):
        self.affects = affects
        # Client persistant
        self.db = chromadb.PersistentClient(path="./alicia_db") 
        self.collection = self.db.get_or_create_collection(name="alicia_memory")
        
        # --- MÉMOIRE VIVE (RAM) ---
        self.memoire_vive = [] 

    def percevoir(self, message_user):
        # 1. Recherche dans les souvenirs déjà consolidés (la DB)
        souvenirs_db = self.collection.query(query_texts=[message_user], n_results=2)
        
        # 2. Calcul de l'importance du message actuel
        importance = self._calculer_importance(message_user)
        
        # 3. Ajout à la RAM (Mémoire de travail)
        self.memoire_vive.append({
            "content": message_user,
            "importance": importance,
            "timestamp": time.time()
        })
        
        # Log console pour que tu vois l'accumulation
        print(f"--- [RAM] {len(self.memoire_vive)}/10 | Import. : {importance:.2f} | Msg: {message_user[:30]}...")

        # 4. Déclenchement de la consolidation si la RAM est pleine
        if len(self.memoire_vive) >= 10:
            self.consolider_vers_db()

        return souvenirs_db['documents']

    def _calculer_importance(self, msg):
        # Les pensées internes dépendent de l'attachement
        if msg == "[Pensée Interne]":
            return 0.1 + (self.affects.state.get('attachement', 0) * 2)
        
        # Les messages de Lo dépendent de la longueur et du nom
        importance = len(msg) / 100.0
        if "Alicia" in msg: importance += 0.2
        return importance

    def consolider_vers_db(self):
        """Transfère les souvenirs forts vers le disque et oublie le reste."""
        print(f"\n--- 🧠 [CONSOLIDATION] Alicia analyse ses 10 derniers fragments... ---")
        sauvegardes = 0
        
        for item in self.memoire_vive:
            # Seuil de survie : 0.35 (ajustable)
            if item['importance'] > 0.35:
                self.collection.add(
                    documents=[item['content']],
                    metadatas=[{
                        "importance": item['importance'], 
                        "timestamp": item['timestamp'],
                        "type": "pensee" if item['content'] == "[Pensée Interne]" else "echange"
                    }],
                    ids=[f"mem_{random.randint(0,99999)}"]
                )
                sauvegardes += 1
                logger_config.logger.info(f"💾 ANCRÉ : {item['content'][:50]} (Imp: {item['importance']:.2f})")
            else:
                logger_config.logger.info(f"💨 OUBLIÉ : {item['content'][:30]}... (Imp: {item['importance']:.2f})")
        
        print(f"--- [FIN] {sauvegardes} souvenirs sauvegardés, {10 - sauvegardes} évaporés. ---\n")
        self.memoire_vive = [] # Reset de la RAM

    def grand_menage_nocturne(self):
        """Nettoyage profond de la DB (Bouton Dodo)."""
        self.consolider_vers_db() # On vide la RAM d'abord
        hier = time.time() - 86400
        try:
            # On supprime ce qui est vieux ET peu important
            self.collection.delete(where={"$and": [
                {"timestamp": {"$lt": hier}},
                {"importance": {"$lt": 0.5}}
            ]})
            return True
        except:
            return False