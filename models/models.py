from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, constr

class Profile(BaseModel):
    id: UUID = None
    login: str
    password: constr(min_length=8) # type: ignore
    name: str
    surname: str
    patronym: str
    email: EmailStr
    birthday: datetime
    experience: int
