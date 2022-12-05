from configparser import ConfigParser
import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, status, responses, File, UploadFile
from fastapi.security import HTTPBasicCredentials, HTTPBasic
import secrets

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
    """
    Function that is used to validate the username in the case that it requires it
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
    return {"message": "Hello World!"}


@app.get("/secured/")
async def secured_function(access: bool = Depends(has_access)):
    new_object = module_class.sample_class()
    result = new_object.sample_method()
    return {"Access": result}


@app.get("/sendfile/")
async def send_file():
    return responses.FileResponse(sample_file)


@app.post("/postfile/")
async def post_file(
    file_to_process: UploadFile = File(...), access: bool = Depends(has_access)
):
    file_location = f"files/{file_to_process.filename}"
    print(file_location)
    with open(file_location, "wb+") as file_object:
        file_object.write(file_to_process.file.read())

    return {"message": "file_sent"}


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.environ["UVICORN_PORT"]),
        log_level="debug",
        reload="true",
    )
