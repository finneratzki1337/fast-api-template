"""Template for FastAPI deployment with some sample methods to be used."""
import os
import secrets
from configparser import ConfigParser

import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, responses, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# importing own modules
from module_template import module_class

# MY_ENV_VAR = os.getenv('MY_ENV_VAR')

# reading potential config
config = ConfigParser()
config.read("config/conf.conf")


if "AM_I_IN_A_DOCKER_CONTAINER" not in os.environ:
    load_dotenv()

# Reading necessary info from environment or config
user_name = os.environ["USER_NAME"]
password = os.environ["USER_PASSWORD"]


sample_file = config["GENERAL"]["SAMPLE_FILE"]


# Initializing FASTAPI APP
app = FastAPI()
security = HTTPBasic()


def has_access(credentials: HTTPBasicCredentials = Depends(security)):
    """Function to validate credentials.

    Can be used by function call on specific routes to check
    whether credentials have been provided during API call.
    Credentials can be defined in .env file.
    """
    correct_username = secrets.compare_digest(credentials.username, user_name)
    correct_password = secrets.compare_digest(credentials.password, password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )

    return True


@app.get("/")
async def root():
    """Function on main route."""
    return {"msg": "Hello World!"}


@app.get("/secured/")
async def secured_function(access: bool = Depends(has_access)):
    """Sample for function that is protected by credentials.add()

    During function call has_access function is called which refers to credentials.
    This method also demonstrated how to access the any underlying modules.
    """
    new_object = module_class.SampleClass()
    result = new_object.sample_method_one()
    return {"Access": result}


@app.get("/sendfile/")
async def send_file():
    """Sends a file to the user.

    Returns:
        fastapi.responses.FileResponse: specified file from config or defined here
    """
    return responses.FileResponse(sample_file)


@app.post("/postfile/")
async def post_file(
    file_to_process: UploadFile = File(...), access: bool = Depends(has_access)
):
    """Function to post file secured by credentials.

    Args:
        file_to_process (UploadFile, optional): _description_. Defaults to File(...).
        access (bool, optional): _description_. Defaults to Depends(has_access).

    Returns:
        json: returns confirmation that file has been received.
    """
    file_location = f"files/{file_to_process.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file_to_process.file.read())

    return {"msg": "file received"}


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.environ["UVICORN_PORT"]),
        log_level="debug",
        reload="true",
    )
