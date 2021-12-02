from sqlalchemy.orm import Session
import hashlib, os

import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    salt = os.urandom(32)
    hashed_pass = hashlib.pbkdf2_hmac(
        'sha256',
        user.password.encode('utf-8'),
        salt,
        100000 # It is recommended to use at least 100,000 iterations of SHA-256 
    )
    hashed_pass += salt
    db_user = models.User(email=user.email, hashed_password=hashed_pass)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_computer(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Computer).offset(skip).limit(limit).all()


def create_computer(db: Session, item: schemas.ComputerCreate):
    db_item = models.Computer(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item