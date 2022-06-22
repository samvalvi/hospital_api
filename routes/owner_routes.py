from fastapi import APIRouter, HTTPException, Response
from models.owner import owner as owner_model
from schemas.owner import OwnerCreate, UpdateOwner, Owner
from db.config import database
from uuid import uuid4
from starlette import status
from bcrypt import hashpw, gensalt
from typing import List

owner_router = APIRouter()


@owner_router.get("/get/all/owners", response_model=List[Owner], tags=["Owner"])
async def get_all_owners(response: Response):
    response.status_code = status.HTTP_200_OK
    query = owner_model.select()
    owners = await database.fetch_all(query)
    return owners


@owner_router.get("/get/owner/{_id}", status_code=status.HTTP_200_OK, response_model=Owner, tags=["Owner"])
async def get_owner(_id: str, response: Response):
    response.status_code = status.HTTP_200_OK
    query = owner_model.select().filter_by(owner_id=_id)
    result = await database.fetch_one(query)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner not found")

    return result


@owner_router.post("/create/owner", response_model=dict, tags=["Owner"])
async def create_owner(data: OwnerCreate, response: Response):
    response.status_code = status.HTTP_201_CREATED
    query = owner_model.select().where(owner_model.c.email == data.email)
    owner_exist = await database.fetch_one(query)

    if owner_exist is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Owner already exists")

    owners_id = str(uuid4())
    hashed_password = hashpw(data.password.encode('utf-8'), gensalt())
    query_insert = owner_model.insert().values(owner_id=owners_id, full_name=data.full_name, email=data.email,
                                               phone=data.phone, address=data.address, password=hashed_password)

    await database.execute(query_insert)

    return {"message": "Owner created"}


@owner_router.put("/update/owner/{_id}", response_model=dict, tags=["Owner"])
async def update_owner(_id: str, data: UpdateOwner, response: Response):
    response.status_code = status.HTTP_200_OK
    exist = owner_model.select().filter_by(owner_id=_id)
    owner_exist = await database.fetch_one(exist)

    if not owner_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner not found")

    query = owner_model.update().where(owner_model.c.owner_id == _id).values(full_name=data.full_name, email=data.email,
                                                                             phone=data.phone, address=data.address)

    await database.execute(query)

    return {"message": "Owner updated"}


@owner_router.delete("/delete/owner/{_id}", response_model=dict, tags=["Owner"])
async def delete_owner(_id: str, response: Response):
    response.status_code = status.HTTP_200_OK
    exist = owner_model.select().filter_by(owner_id=_id)
    owner_exist = await database.fetch_one(exist)

    if not owner_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner not found")

    query = owner_model.delete().where(owner_model.c.owner_id == _id)

    await database.execute(query)

    return {"message": "Owner deleted"}
