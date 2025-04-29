
from fastapi import FastAPI, Query
from datetime import datetime
import swisseph as swe

app = FastAPI()

nakshatras = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

vimshottari_order = [
    ("Ketu", 7), ("Venus", 20), ("Sun", 6), ("Moon", 10), ("Mars", 7),
    ("Rahu", 18), ("Jupiter", 16), ("Saturn", 19), ("Mercury", 17)
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

@app.get("/moon_nakshatra_dasa")
def get_moon_nakshatra_dasa(
    date: str = Query(..., example="2025-04-29T18:00"),
    latitude: float = Query(..., example=48.98),
    longitude: float = Query(..., example=2.2)
):
    dt = datetime.fromisoformat(date)
    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0)
    swe.set_topo(longitude, latitude, 0)
    moon_lon, _ = swe.calc_ut(jd, swe.MOON)[0:2]

    nak_index = int(moon_lon // (360 / 27))
    pada = int((moon_lon % (360 / 27)) // (360 / 108)) + 1
    nakshatra = nakshatras[nak_index]

    dasa_planet = nakshatra_to_planet[nakshatra]
    appearance_count = 0

    # Get Bukti using the planet's sky-ordered nakshatras
    planet_naks = planet_to_nakshatras[dasa_planet]
    bukti_index = appearance_count % len(planet_naks)
    bukti = planet_naks[bukti_index]

    return {
        "nakshatra": nakshatra,
        "moon_longitude": round(moon_lon, 4),
        "pada": pada,
        "dasa": dasa_planet,
        "bukti": bukti,
        "start_time": dt.strftime("%d/%m/%Y %H:%M:%S")
    }
