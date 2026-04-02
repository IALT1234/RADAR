from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
import models
from typing import Annotated
from db import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class UserBase(BaseModel):
    username: str


def get_db():
    db = SessionLocal()
    try:
        yield db

    finally: 
        db.close()


@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()




@app.get("/hello")
def hello():
    return {"message": "Hello from FastAPI"}

@app.get("/register")
def register():
    return 