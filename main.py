from datetime import time

from fastapi import FastAPI, Depends
from sqlalchemy.dialects.postgresql import psycopg2
from sqlalchemy.orm import Session

import models
from database import engine, get_db
from schemas import Products

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='ecommerce', user='postgres',
                                password='admin', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database succesfully connected')
        break
    except Exception as error:
        print('connection failed')
        print('error:', error)
        time.sleep(3)

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def posts():
    return {"message": "this is working"}


@app.post("/product")
def create(product: Products, db: Session = Depends(get_db)):
    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
