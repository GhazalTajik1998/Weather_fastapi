import logging
import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from beanie.odm.utils.init import init_beanie

from motor.motor_asyncio import AsyncIOMotorClient
import uvicorn

from api.weather import weather_api 
from core.config import settings
from models.user_model import User
from api.router import router

def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    return application

app = get_application()

def run_application():
    try:
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
        )
    except Exception as e:
        logging.error("An error occured while running the application")
        logging.exception(e)


def configure():
    configure_routing()
    configure_api_keys()

def configure_api_keys():
    file = Path('settings.json').absolute()
    if not file.exists():
        raise Exception("settings.json file not found, you cannot continue, please see settings_template.json")
    with open(file) as fin:
        settings = json.load(fin)
        weather_api.api_key = settings.get('api_key')

def configure_routing():  
    app.include_router(router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def app_init():
    db = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING, uuidRepresentation="standard")
    db = db["weather"]
    await init_beanie(
        database = db,
        document_models = [
            User,
        ]
    )


if __name__ == "__main__":
    configure() 
    run_application()
 
else: 
    configure()
      