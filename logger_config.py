import logging

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] Alicia-Internal: %(message)s',
    handlers=[
        logging.FileHandler("alicia_mind.log", encoding="utf-8"), # Ajoute l'encoding ici !
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("Alicia")

# Exemple d'utilisation dans ton code :
# logger.info(f"ADN chargé avec succès : {dna[:8]}...")
# logger.warning("Tension élevée détectée (0.9)")