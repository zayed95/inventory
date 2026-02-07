import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

# Add middleware to allow the frontend running on prt 3000 to communicate with the backend on port 8000
app.add_middleware(
    CORSMiddleware,
    allow_origins=['https://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

load_dotenv()

redis = get_redis_connection(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True
)

class Product(HashModel, index=True):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get("/products")
def all():
    return [Product.get(pk) for pk in Product.all_pks()]


@app.post('/products')
def create(product: Product):
    return product.save()

@app.get('/products/{pk}')
def get_product(pk: str):
    return Product.get(pk)

@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)