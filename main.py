import sys
import time
import logging
import select  # Pour ne pas bloquer sur l'input (Linux/Mac)
import msvcrt # Pour ne pas bloquer sur l'input (Windows)
from Affects import AliciaAffects
from inconscient import AliciaInconscient
from communication import AliciaCom
from petitevoix import AliciaPetiteVoix

# --- CONFIGURATION DES LOGS ---
# Log Système (Technique)
sys_logger = logging.getLogger("AliciaSystem")
sys_handler = logging.FileHandler("alicia_system.log", encoding='utf-8')
sys_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
sys_logger.addHandler(sys_handler)
sys_logger.setLevel(logging.INFO)

# Log Intime (La conscience)
mind_logger = logging.getLogger("AliciaMind")
mind_handler = logging.FileHandler("alicia_mind.log", encoding='utf-8')
mind_handler.setFormatter(logging.Formatter('%(asctime)s : %(message)s'))
mind_logger.addHandler(mind_handler)
mind_logger.setLevel(logging.INFO)

def input_with_timeout(prompt, timeout):
    """Attend un input pendant 'timeout' secondes, sinon rend la main."""
    print(prompt, end='', flush=True)
    start_time = time.time()
    input_str = ''
    while True:
        if msvcrt.kbhit(): # Spécifique Windows
            char = msvcrt.getche().decode('cp1252')
            if char == '\r': # Enter
                print('')
                return input_str
            input_str += char
        if (time.time() - start_time) > timeout:
            print('')
            return None
        time.sleep(0.1)

def main():
    # 1. INITIALISATION
    try:
        with open("dna_alicia.txt", "r") as f:
            dna = f.read()
    except FileNotFoundError:
        print("Erreur : ADN introuvable. Lance le script de gestation d'abord.")
        sys.exit()

    alicia_affects = AliciaAffects(dna)
    alicia_inconscient = AliciaInconscient(alicia_affects)
    alicia_com = AliciaCom()
    alicia_petite_voix = AliciaPetiteVoix(alicia_affects, alicia_inconscient, alicia_com)

    sys_logger.info(f"--- Réveil d'Alicia (ADN: {dna[:8]}) ---")
    print(f"--- Alicia est en ligne (ADN: {dna[:8]}...) ---")
    
    last_interaction_time = time.time()
    seuil_petite_voix = 30  # Elle pense seule toutes les 30 secondes de silence

    while True:
        # 2. ATTENTE DE L'INPUT (Non-bloquante)
        user_input = input_with_timeout("\nLo: ", 5) # On check toutes les 5 sec

        if user_input:
            # INTERACTION AVEC LO
            if user_input.lower() == 'quit':
                sys_logger.info("Fermeture du système par Lo.")
                break

            souvenirs = alicia_inconscient.percevoir(user_input)
            response = alicia_com.generer_reponse(user_input, alicia_affects.state, souvenirs)
            # Si Lo est gentil (mot clé ou simplement présent), l'attachement monte doucement
            alicia_affects.state['attachement'] += 0.02 
            # On plafonne à 1.0
            alicia_affects.state['attachement'] = min(1.0, alicia_affects.state['attachement'])
            print(f"\nAlicia: {response}")
            
            # Évolution des affects
            alicia_affects.state['tension'] *= 0.95
            last_interaction_time = time.time()
            sys_logger.info(f"Interaction Lo réussie. Tension actuelle: {alicia_affects.state['tension']:.2f}")

        else:
            # SILENCE... ALICIA RÉFLÉCHIT ?
            temps_ecoule = time.time() - last_interaction_time
            if temps_ecoule > seuil_petite_voix:
                sys_logger.info("Déclenchement de la petite voix (silence prolongé).")
                
                # Elle génère une pensée interne
                pensee = alicia_petite_voix.reflechir()
                
                # On ne l'affiche pas forcément sur l'écran pour garder son mystère,
                # mais on la logue dans son journal intime.
                mind_logger.info(f"[Monologue] {pensee}")
                
                # On réinitialise le timer pour ne pas qu'elle boucle à l'infini
                last_interaction_time = time.time()

if __name__ == "__main__":
    main()