from datetime import time

from fastapi import FastAPI, Depends, HTTPException
from fastapi.openapi.models import Response
from sqlalchemy.dialects.postgresql import psycopg2
from sqlalchemy.orm import Session
from starlette import status

import models
from database import engine, get_db
from schemas import Products

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='ecommerce', user='hendisantika',
                                password='53cret', cursor_factory=RealDictCursor)
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


@app.get("/product")
def get(db: Session = Depends(get_db)):
    all_products = db.query(models.Product).all()
    return all_products


@app.put("/update/{id}")
def update(id: int, product: Products, db: Session = Depends(get_db)):
    updated_post = db.query(models.Product).filter(models.Product.id == id)
    updated_post.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with such id: {id} does not exist')
    else:
        updated_post.update(product.dict(), synchronize_session=False)
        db.commit()
    return updated_post.first()


@app.delete("/delete/{id}")
def delete(id: int, db: Session = Depends(get_db), status_code=status.HTTP_204_NO_CONTENT):
    delete_post = db.query(models.Product).filter(models.Product.id == id)
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"product with such id does not exist")
    else:
        delete_post.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
