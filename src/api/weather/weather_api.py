import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from fastapi import APIRouter, Depends
from typing import Optional
from services.weather_services import connect_api
from api.dependency.user_deps import get_current_user
from models.user_model import User

weather_router = APIRouter()
api_key: Optional[str] = None


async def get_geo_by_city(city: str, country: Optional[str] = None) -> Optional[str]:
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{country}&appid={api_key}"
    data = await connect_api(url)

    if data:
        lat = data[0].get('lat', None)
        lon = data[0].get('lon', None)
        return f"lat={lat}&lon={lon}"
    else: 
        return None

@weather_router.get("/current/{city}", summary="Get current weather")
async def get_current_weather(city:str,
                                country: Optional[str] = None,
                                current_user: User = Depends(get_current_user)) -> dict:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}"
    data = await connect_api(url)

    fields = ['coord', 'weather', 'main', 'wind', 'clouds','dt', 'sys', 'name']
    cleaned_data = {key:data.get(key, None) for key in fields}
    return cleaned_data


@weather_router.get("/pollution/{city}", summary="Get pollution of city")
async def get_polluted(city: str,
                        country: Optional[str] = None,
                        current_user: User = Depends(get_current_user)) -> dict:
    
    geo_info = await get_geo_by_city(city, country)
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?{geo_info}&appid={api_key}"

    data = await connect_api(url)
    cleaned_data = data | {"city" : city}
    return cleaned_data