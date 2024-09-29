check-codestyle-ruff:
	poetry run ruff check --output-format=github .
	poetry run ruff format --diff .

fix-codestyle:
	poetry run ruff check --fix --unsafe-fixes .
	poetry run ruff format .

populate-data:
	poetry run python import_data.py
