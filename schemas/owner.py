from pydantic import BaseModel


class OwnerBase(BaseModel):
    full_name: str
    email: str
    phone: str
    address: str

    class Config:
        orm_mode = True


class OwnerCreate(OwnerBase):
    password: str


class UpdateOwner(OwnerBase):
    pass


class Owner(OwnerBase):
    owner_id: str

    class Config:
        orm_mode = True
