from typing import List, Optional
import datetime

from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import DateTime

class ComputerBase(BaseModel):
    type: str
    used: bool

class ComputerCreate(ComputerBase):
    last_active: datetime.datetime


class Computer(ComputerBase):
    id: int
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Computer] = []

    class Config:
        orm_mode = True