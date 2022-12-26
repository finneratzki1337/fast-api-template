FROM ubuntu
ARG DEBIAN_FRONTEND=noninteractive
ENV AM_I_IN_A_DOCKER_CONTAINER Yes
#Updating on every build for security
RUN apt-get update
RUN apt-get install -y wget
RUN apt-get install -y python3 && apt-get install -y python3-pip
RUN apt-get install -y uvicorn
WORKDIR /code

#Or specifically adding requirements txt only
COPY requirements.txt .
#COPY app.py .

RUN pip3 install -r requirements.txt
RUN useradd -ms /bin/bash exec-user
#Switching user for security reasons

ADD . /code
RUN chown exec-user files
USER exec-user

CMD uvicorn app:app --host 0.0.0.0 --port ${UVICORN_PORT} --workers ${NUMBER_WORKERS}
