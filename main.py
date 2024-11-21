from datetime import time

from fastapi import FastAPI
from sqlalchemy.dialects.postgresql import psycopg2

import models
from database import engine

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
