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
    with open("emotional_matrix.json", "r") as f:
        return json.load(f)

@app.get("/api/private/{user_id}")
def get_private_layer(user_id: str):
    if user_id != "patd315":
        raise HTTPException(403, "Private layer denied.")
    path = f"layers/{user_id}.json"
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)
