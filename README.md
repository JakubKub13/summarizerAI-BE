Simple FastAPI app that summarizes text using OpenAI api models.

## Installation
After cloning repo from Github create python3 virtual environment with command: python3 -m venv venv.
Than activate the python3 virtual environment by command: source venv/bin/activate. 
Than run: pip install -r requirements. txt to install all dependencies.

Also you need to create a .env from .env.example file in the root directory of the project and add the missing variables:

## Usage
Make sure you have postgreSQL installed and running on your machine.
Create a local database. 
After everything is set up run python3 main.py to start the server.

You can access the app and test the endpoint using Swagger documentation at http://0.0.0.0:8833/docs# summarizerAI-BE
