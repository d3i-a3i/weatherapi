from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:44337"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

API_KEY = "107fe439bfbba6d710d6d43c4da562f8"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather?q=Montpellier&appid=" + API_KEY + "&units=metric"

@app.get("/compare_temperature/{input_temperature}")
@CORSMiddleware(
    app=app,
    allow_origins=["https://s3i-flutter.web.app"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
async def compare_temperature(input_temperature: float):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(WEATHER_URL)
            response.raise_for_status()
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=500, detail="Problème de récupération des données météo.")

        weather_data = response.json()
        current_temperature = weather_data["main"]["temp"]
#l'api renvoie 
        # OUI SI
        # la température actuelle de Montpellier est inférieure à la température 
        # saisie par l'utilisateur
        
        return "OUI" if input_temperature < current_temperature else "NON"
