import os
from dotenv import load_dotenv
from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel

app = FastAPI()

load_dotenv()

redis = get_redis_connection(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True
)

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get("/products")
async def all():
    return []
