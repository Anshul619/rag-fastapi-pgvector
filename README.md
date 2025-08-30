# Quick start

## Setup environment variables
- Copy the example environment file and update it as needed
- Add **GEMINI_API_KEY** if you want generative answers

````shell
cp .env.example .env
````

## Import DB SqL
- `sql/init.sql` in postgres db

## Start the database

````shell
docker compose up -d db
````

## Create and activate virtual environment

````shell
python3 -m venv venv
source .venv/bin/activate
````

## Install dependencies

````shell
pip install -r requirements.txt
````

## Configure environment
- Unset any existing database URL to avoid conflicts

````shell
unset DATABASE_URL
````

Load variables from .env

````shell
source .env
````

## Run the API server

````shell
uvicorn app.main:app --reload --port 8000
````

## Ingest a document

````shell
curl -X POST http://localhost:8000/ingest \
-H "Content-Type: application/json" \
-d '{"title":"Sample","text":"FastAPI is a modern, fast web framework..."}'

curl -X POST http://localhost:8000/ingest \
-H "Content-Type: application/json" \
-d '{"title":"Sample","text":"FastAPI is a modern, fast web framework... game is pay. Another sentence here. And one more sentence to chunk."}'
````

## Query the database

````shell
curl -X POST http://localhost:8000/query \
-H "Content-Type: application/json" \
-d '{"question":"What does the document say about FastAPI?", "top_k": 5}'
````