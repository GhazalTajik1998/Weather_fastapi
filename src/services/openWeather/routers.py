from typing import Optional

from fastapi import Depends, APIRouter, Request

from .api_utils import connect_api



api_key: Optional[str] = None


router = APIRouter()

async def get_city_by_geo(lat: str, lon: str, api_key: str):
    limit = 4
    url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit={limit}&appid={api_key}"
    data = await connect_api(url)
    if data:
        name = data[0].get("name")
        country = data[0].get("country")
        return (name, country)
    else: 
        return None

@router.get("/api/weather/{city}")
async def get_current_weather(city:str, country: Optional[str] = None):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}"
    data = await connect_api(url)

    return data


@router.get("/api/forcast/{city}")
async def get_forcast_city(city:str, country: Optional[str] = "US"):
    url = f"https://pro.openweathermap.org/data/2.5/forecast/hourly?q={city},{country}&appid={api_key}"
    data = await connect_api(url)


@router.get("/api/pollution/{lat}/{lon}")
async def get_polluted(lat: str, lon: str):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&limit=5&appid={api_key}"

    data = await connect_api(url)

