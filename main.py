import time
from typing import Annotated

import psycopg2
from fastapi import FastAPI, Depends, HTTPException, Response
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from starlette import status

import config
import models
from database import engine, get_db
from schemas import Products

DbSession = Annotated[Session, Depends(get_db)]

while True:
    try:
        conn = psycopg2.connect(host=config.DB_HOST, port=config.DB_PORT, database=config.DB_NAME,
                                user=config.DB_USER, password=config.DB_PASSWORD,
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database succesfully connected')
        break
    except Exception as error:
        print('connection failed')
        print('error:', error)
        time.sleep(3)

app = FastAPI(
    title="FastAPI CRUD Postgres",
    description="A simple CRUD REST API for managing products, "
                "built with FastAPI, SQLAlchemy, and PostgreSQL.",
    version="1.0.0",
    contact={
        "name": "Hendi Santika",
        "email": "hendisantika@yahoo.co.id",
        "url": "https://github.com/hendisantika/fastapi-crud-postgres",
    },
    license_info={
        "name": "MIT License",
    },
)

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def posts():
    return {"message": "this is working"}


@app.post("/product")
def create(product: Products, db: DbSession):
    new_product = models.Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.get("/product")
def get(db: DbSession):
    all_products = db.query(models.Product).all()
    return all_products


@app.put("/update/{id}")
def update(id: int, product: Products, db: DbSession):
    updated_post = db.query(models.Product).filter(models.Product.id == id)
    if updated_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'product with such id: {id} does not exist')
    updated_post.update(product.model_dump(), synchronize_session=False)
    db.commit()
    return updated_post.first()


@app.delete("/delete/{id}")
def delete(id: int, db: DbSession):
    delete_post = db.query(models.Product).filter(models.Product.id == id)
    if delete_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"product with such id: {id} does not exist")
    delete_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
