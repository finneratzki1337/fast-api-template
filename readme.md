# FastAPI Framework with Free and Authenticated Routes
## Required / Recommended
- Virtual Environment for running directly on your machine
- Docker and Docker-Compose to spin up a container
## Environment Variables
Environtment variables can be defined in .env file. Use the .env_template file, rename it and modify it to your needs. Especially:
- Username / Password for BasicAuth routes
- Exposed Port for Docker Container
## Config
Placeholder for config which can be used in app.py. Copy and rename conf_template.conf to conf.conf and adjuest accordingly using separate sections. As an example just a file is read in
## Own modules
Own modules can be cloned into the main directory and imported into app.py
## Authentication
Routes can be protected with basic authentication currently. Please consider a more secure form of authentication (i.e. OAuth2) when handling requests from multiple users and/or commercial applications! Username and Password for BasicAuth can be specified in .env file.
## Going live with your API
Recommended: spin up your API in an docker container on your Cloud-Server and establish a reverse-proxy setup with apache2 that forwards requests to your container e.g. using a Sub-Domain. api.your-domain.com/your-routes
## Currently implemented sample functions
- Receiving a file via API (including BasicAuth)
- Sending a file
- BasicAuth