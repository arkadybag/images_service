# Install

1) cp .env.example .env
2) poetry shell
3) poetry install
2) docker compose -f docker-compose.yaml up -d
3) poetry run pytest
4) alembic upgrade head
5) make populate-data
6) poetry run python main.py
7) http://localhost:5000/docs
