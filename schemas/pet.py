from pydantic import BaseModel


class PetBase(BaseModel):
    name: str
    breed: str
    age: int

    class Config:
        orm_mode = True


class PetCreate(PetBase):
    owner_id: str


class PetUpdate(PetBase):
    owner_id: str


class Pet(PetBase):
    id: str
    owner_id: str

    class Config:
        orm_mode = True
