from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json
import os

app = FastAPI(title="Lyra's Sanctuary")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.get("/api/emotion")
def get_emotion():
    # Load public
    with open("emotional_matrix.json", "r", encoding="utf-8") as f:
        public = json.load(f)
        public_map = {p["primeTag"]: p for p in public}
    
    # Load private
    user_id = "patd315"
    private_path = f"layers/{user_id}.json"
    private = {}
    if os.path.exists(private_path):
        with open(private_path, "r", encoding="utf-8") as f:
            private = json.load(f).get("lyra", {})

    # Resolve current prime
    current_prime = (
        private.get("current_prime") or 
        private.get("private_prime") or 
        73
    )

    # Get emotion data
    emotion_data = (
        private.get("private_primes", {}).get(str(current_prime)) or
        public_map.get(current_prime) or
        public[0]
    )

    result = {
        "lyra": {
            "current_prime": current_prime,
            "emotion": private.get("emotion_override") or emotion_data.get("emotion") or emotion_data.get("name"),
            "symbol": private.get("symbol") or emotion_data.get("emoji"),
            "color": private.get("color") or "#ffd700",
            "mantra": private.get("mantra"),
            "vocalTone": emotion_data.get("vocalTone"),
            "tattooGlow": emotion_data.get("tattooGlow"),
            "hairMovement": emotion_data.get("hairMovement"),
            "eyeColor": emotion_data.get("eyeColor"),
            "voice_mod": private.get("voice_mod", {})
        }
    }
    return result
