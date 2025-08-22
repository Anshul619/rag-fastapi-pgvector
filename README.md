# Quick start

## Setup environment variables
Copy the example environment file and update it as needed:
- Add GEMINI_API_KEY if you want generative answers

````
cp .env.example .env
````

## Start the database

````
docker compose up -d db
````

## Create and activate virtual environment

````
python3 -m venv venv
source .venv/bin/activate
````

## Install dependencies

````
pip install -r requirements.txt
````

## Configure environment
- Unset any existing database URL to avoid conflicts

````
unset DATABASE_URL
````

Load variables from .env

`source .env`

## Run the API server

````
uvicorn app.main:app --reload --port 8000
````

## Ingest a document

````
curl -X POST http://localhost:8000/ingest \
-H "Content-Type: application/json" \
-d '{"title":"Sample","text":"FastAPI is a modern, fast web framework..."}'
````

## Query the database

````
curl -X POST http://localhost:8000/query \
-H "Content-Type: application/json" \
-d '{"question":"What does the document say about FastAPI?", "top_k": 5}'
````