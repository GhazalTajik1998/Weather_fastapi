import logging

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

import uvicorn


def get_application() -> FastAPI:
    application = FastAPI()

    return application




app = get_application()

def run_application():
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
        )
    except Exception as e:
        logging.error("An error occured while running the application")
        logging.exception(e)


if __name__ == "__main__":
    run_application()
    