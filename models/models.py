from datetime import datetime
from pydantic import BaseModel, EmailStr, constr

class Profile(BaseModel):
    id: int = None
    login: str = None
    password: constr(min_length=8) = None # type: ignore
    name: str = None
    surname: str = None
    patronym: str = None
    email: EmailStr = None
    birthday: datetime = None
    age: datetime = None
    experience: int = None
