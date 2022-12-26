"""Template for FastAPI deployment with some sample methods to be used."""
import os
from configparser import ConfigParser

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

# importing own modules
from src.routers import sample_methods

# MY_ENV_VAR = os.getenv('MY_ENV_VAR')

# reading potential config
config = ConfigParser()
config.read("config/conf.conf")


if "AM_I_IN_A_DOCKER_CONTAINER" not in os.environ:
    load_dotenv()

# Initializing FASTAPI APP
app = FastAPI()
app.include_router(sample_methods.router)

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.environ["UVICORN_PORT"]),
        log_level="debug",
        reload="true",
    )