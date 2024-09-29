import asyncio
import csv

from app.image_processing.import_data import import_data
from settings import Settings


async def import_initial_data():
    settings = Settings()
    with open("app/initial_data/img.csv") as f:
        data = list(csv.reader(f))

    await import_data(settings, data[1:])


asyncio.run(import_initial_data())
