FROM python:3.12.2 as requirements-stage

WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.12.2-slim
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /code
WORKDIR /code
ENV PYTHONPATH=/code
EXPOSE 5001
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "5000", "--workers", "1"]