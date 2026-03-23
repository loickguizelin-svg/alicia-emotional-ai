from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import json
import os
import time

from Affects import AliciaAffects
from inconscient import AliciaInconscient
from communication import AliciaCom
from petitevoix import AliciaPetiteVoix

app = FastAPI()
templates = Jinja2Templates(directory="templates")

STATE_FILE = "etat_alicia.json"

def charger_etat():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'tension': 0.2, 'energie': 1.0, 'curiosite': 0.05, 'attachement': 0.0, 'entropie': 0.0, 'stabilite': 1.0}

def sauvegarder_etat():
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(alicia_affects.state, f, ensure_ascii=False, indent=4)

# Initialisation
constantes_vitales = charger_etat()
alicia_affects = AliciaAffects(constantes_vitales)
alicia_inconscient = AliciaInconscient(alicia_affects)
alicia_com = AliciaCom()
alicia_petite_voix = AliciaPetiteVoix(alicia_affects, alicia_inconscient)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "dna": "ALICIA-CORE-V2"})

@app.post("/chat")
async def chat(message: str = Form(...)):
    # 1. Perception (Gère la RAM et la Consolidation auto)
    souvenirs = alicia_inconscient.percevoir(message)
    
    # 2. Génération
    response = alicia_com.generer_reponse(message, alicia_affects.state, souvenirs)
    
    # 3. Mise à jour des affects
    alicia_affects.state['tension'] *= 0.95
    alicia_affects.state['attachement'] = min(1.0, alicia_affects.state['attachement'] + 0.01)
    
    # 4. Sauvegarde
    sauvegarder_etat()
    
    return {
        "user": message, 
        "alicia": response, 
        "affects": alicia_affects.state,
        "ram_status": f"{len(alicia_inconscient.memoire_vive)}/10"
    }

@app.post("/sleep")
async def simulation_sommeil():
    succes = alicia_inconscient.grand_menage_nocturne()
    # Sommeil réparateur
    alicia_affects.state['tension'] = 0.05
    alicia_affects.state['energie'] = 1.0
    sauvegarder_etat()
    return {"status": "Alicia a dormi. Sa mémoire est consolidée.", "success": succes}

@app.get("/affects")
async def get_affects():
    return alicia_affects.state

# --- Logique des murmures ---
pensees_publiques = []

@app.get("/notifications")
async def get_notifications():
    global pensees_publiques
    current_thoughts = list(pensees_publiques)
    pensees_publiques = [] 
    return {"thoughts": current_thoughts}

def boucle_petite_voix():
    while True:
        time.sleep(60) 
        pensee = alicia_petite_voix.reflechir()
        # On passe la pensée à l'inconscient pour la RAM
        alicia_inconscient.percevoir("[Pensée Interne]") 
        pensees_publiques.append(pensee)
        if len(pensees_publiques) > 5:
            pensees_publiques.pop(0)

import threading
threading.Thread(target=boucle_petite_voix, daemon=True).start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)