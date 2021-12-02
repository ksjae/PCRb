from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

origins = [
    "http://127.0.0.1",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

computer_list = []
max_id=10

def find_new_id(id_list: list):
    for i in range(len(id_list)+5): # I doubt my abilities
        if i not in id_list:
            return i

@app.get("/")
async def root():
    return {"message": max_id - len(computer_list)}

@app.post("/")
async def add_computer(id: Optional[int] = None):
    if not id:
        id = find_new_id(computer_list)
        computer_list.append(id)
        return {"message": id}
    return {"message": "refreshed"}




@app.get("/seats/by_type")
async def list_by_type():
    return {"premium": "1", "standard": "2", "economy": "3"}

@app.get("/seats/", response_model=List[schemas.Computer])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_computer(db, skip=skip, limit=limit)
    return items

@app.post("/seats/", response_model=schemas.Computer)
def create_computer(
    item: schemas.ComputerCreate, db: Session = Depends(get_db)
):
    return crud.create_computer(db=db, item=item)




@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user