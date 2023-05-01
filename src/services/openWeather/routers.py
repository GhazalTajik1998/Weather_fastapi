from typing import Optional

from fastapi import Depends, APIRouter, Request

from .api_utils import connect_api



api_key: Optional[str] = None
router = APIRouter()

async def get_geo_by_city(city: str, country: Optional[str] = None) -> Optional[str]:

    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{country}&appid={api_key}"
    data = await connect_api(url)
    if data:
        lat = data[0].get('lat', None)
        lon = data[0].get('lon', None)
        return f"lat={lat}&lon={lon}"
    else: 
        return None

@router.get("/api/weather/{city}")
async def get_current_weather(city:str, country: Optional[str] = None) -> dict:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}"
    data = await connect_api(url)

    fields = ['coord', 'weather', 'main', 'wind', 'clouds','dt', 'sys', 'name']
    cleaned_data = {key:data.get(key, None) for key in fields}

    return cleaned_data


@router.get("/api/pollution/{city}")
async def get_polluted(city: str, country: Optional[str] = None) -> dict:
    geo_info = await get_geo_by_city(city, country)

    url = f"http://api.openweathermap.org/data/2.5/air_pollution?{geo_info}&appid={api_key}"

    data = await connect_api(url)
    cleaned_data = data | {"city" : city}

    return cleaned_data

