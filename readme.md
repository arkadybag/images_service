# Run local
1) cp .env.example .env
2) poetry shell
3) poetry install
4) docker compose build
5) docker compose up db -d
6) poetry run pytest
7) alembic upgrade head
8) make populate-data
9) poetry run python main.py
10) http://localhost:5001/docs


# Run docker
1) cp .env.example .env 
2) add into your `.env` this: `POSTGRES_HOST=db`
3) docker compose build
4) docker compose up -d
5) http://localhost:5001/docs

