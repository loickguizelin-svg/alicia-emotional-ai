import hashlib
import json
import os
import random

class AliciaAffects:
    def __init__(self, dna_sequence):
        self.dna = dna_sequence
        # Le décodage de l'ADN en traits de caractère (coefficients fixes)
        self.traits = self._decode_dna(dna_sequence)
        
        # État dynamique (les variables qui vont bouger)
        self.state = {
            "tension": 0.2,      # Calme au démarrage
            "energie": 1.0,      # Batterie pleine
            "curiosite": self.traits['base_curiosity'],
            "attachement": 0.0,   # Tout à construire
            "entropie": 0.0,
            "stabilite": 1.0
        }

    def _decode_dna(self, dna):
        # On utilise le hash de l'ADN pour extraire des valeurs entre 0 et 1
        h = hashlib.sha256(dna.encode()).hexdigest()
        return {
            "base_curiosity": int(h[0:2], 16) / 255.0,
            "patience": int(h[2:4], 16) / 255.0,
            "sensitivity": int(h[4:6], 16) / 255.0,
            "introversion": int(h[6:8], 16) / 255.0
        }

    def save_state(self, path="alicia_state.json"):
        with open(path, 'w') as f:
            json.dump({"dna": self.dna, "state": self.state}, f)

# --- Initialisation du dossier Alicia ---
if not os.path.exists("dna_alicia.txt"):
    # GESTATION : Génération de l'ADN unique
    new_dna = ''.join(random.choices('0123456789ABCDEF', k=64))
    with open("dna_alicia.txt", "w") as f:
        f.write(new_dna)
    print(f"🧬 Alicia est née. ADN généré.")
else:
    with open("dna_alicia.txt", "r") as f:
        new_dna = f.read()
    print(f"👁️ ADN chargé. Alicia se réveille...")

alicia = AliciaAffects(new_dna)
print(f"Tempérament décodé : {alicia.traits}")