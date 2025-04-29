from fastapi import FastAPI, Query
from datetime import datetime

app = FastAPI()

nakshatras = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

planet_to_nakshatras = {
    "Ketu": ["Ashwini", "Magha", "Mula"],
    "Venus": ["Bharani", "Purva Phalguni", "Purva Ashadha"],
    "Sun": ["Krittika", "Uttara Phalguni", "Uttara Ashadha"],
    "Moon": ["Rohini", "Hasta", "Shravana"],
    "Mars": ["Mrigashira", "Chitra", "Dhanishta"],
    "Rahu": ["Ardra", "Swati", "Shatabhisha"],
    "Jupiter": ["Punarvasu", "Vishakha", "Purva Bhadrapada"],
    "Saturn": ["Pushya", "Anuradha", "Uttara Bhadrapada"],
    "Mercury": ["Ashlesha", "Jyeshtha", "Revati"]
}

nakshatra_to_planet = {}
for planet, naks in planet_to_nakshatras.items():
    for nak in naks:
        nakshatra_to_planet[nak] = planet

def approximate_moon_longitude(dt: datetime) -> float:
    # Approximate: Moon moves ~13.2 degrees per day
    base_date = datetime(2025, 4, 28)
    days_diff = (dt - base_date).days
    base_moon_deg = 40.0  # Approx starting near Rohini (40 deg)
    moon_deg = (base_moon_deg + 13.2 * days_diff) % 360
    return moon_deg

@app.get("/moon_nakshatra_dasa")
def get_moon_nakshatra_dasa(
    date: str = Query(..., example="2025-04-29T18:00"),
    latitude: float = Query(..., example=48.98),
    longitude: float = Query(..., example=2.2)
):
    dt = datetime.fromisoformat(date)

    moon_lon = approximate_moon_longitude(dt)

    nak_index = int(moon_lon // (360 / 27))
    pada = int((moon_lon % (360 / 27)) // (360 / 108)) + 1
    nakshatra = nakshatras[nak_index]

    dasa_planet = nakshatra_to_planet.get(nakshatra, "Unknown")
    bukti = planet_to_nakshatras.get(dasa_planet, ["Unknown"])[0]

    return {
        "nakshatra": nakshatra,
        "moon_longitude": round(moon_lon, 2),
        "pada": pada,
        "dasa": dasa_planet,
        "bukti": bukti,
        "start_time": dt.strftime("%d/%m/%Y %H:%M:%S")
    }
