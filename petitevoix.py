import logging
import random

mind_logger = logging.getLogger("AliciaMind")

class AliciaPetiteVoix:
    def __init__(self, affects, inconscient, communication):
        self.affects = affects
        self.inconscient = inconscient
        self.com = communication

    def reflechir(self):
        # 1. Elle pioche un souvenir pour nourrir sa réflexion
        souvenir_lointain = self.inconscient.percevoir("mes pensées profondes")
        
        # 2. Génération de la pensée
        pensee = self.com.generer_reponse("[Pensée Interne]", self.affects.state, souvenir_lointain)
        
        # 3. AUTO-MEMORISATION : Elle écrit sa propre pensée dans son inconscient
        # On utilise une importance fixe ou basée sur la longueur pour que ses réflexions marquent sa mémoire
        self.inconscient.collection.add(
            documents=[f"J'ai pensé : {pensee}"],
            metadatas=[{"origine": "introspection", "tension": self.affects.state['tension']}],
            ids=[f"pensee_{random.randint(0,99999)}"]
        )
        
        return pensee