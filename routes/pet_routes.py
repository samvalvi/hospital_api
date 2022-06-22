from typing import List
from starlette import status
from models.owner import pet as pet_model
from fastapi import APIRouter, Response, HTTPException
from db.config import database
from schemas.pet import PetCreate, PetUpdate, Pet
from uuid import uuid4

pet_router = APIRouter()


@pet_router.get("/get/all/pets", response_model=List[Pet], tags=["Pet"])
async def get_all_pets(response: Response):
    response.status_code = status.HTTP_200_OK
    query = pet_model.select()
    pets = await database.fetch_all(query)
    return pets


@pet_router.get("/get/pet/{pet_id}", response_model=Pet, tags=["Pet"])
async def get_pet(pet_id: str, response: Response):
    response.status_code = status.HTTP_200_OK
    query = pet_model.select().filter_by(id=pet_id)
    result = await database.fetch_one(query)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")

    return result


@pet_router.post("/create/pet", response_model=dict, tags=["Pet"])
async def create_pet(data: PetCreate, response: Response):
    response.status_code = status.HTTP_201_CREATED
    query = pet_model.select().where(pet_model.c.owner_id == data.owner_id and pet_model.c.name == data.name)
    pet_exist = await database.fetch_one(query)

    if pet_exist is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Pet already exist")

    pet_id = str(uuid4())
    query_insert = pet_model.insert().values(id=pet_id, owner_id=data.owner_id, name=data.name,
                                             breed=data.breed, age=data.age)

    await database.execute(query_insert)

    return {"message": "Pet created"}


@pet_router.put("/update/pet/{pet_id}", response_model=dict, tags=["Pet"])
async def update_pet(pet_id: str, data: PetUpdate, response: Response):
    response.status_code = status.HTTP_200_OK
    exist = pet_model.select().filter_by(id=pet_id)
    pet_exist = await database.fetch_one(exist)

    if not pet_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")

    query = pet_model.update().where(pet_model.id == pet_id).values(name=data.name, breed=data.breed, age=data.age,
                                                                    owner_id=data.owner_id)
    await database.execute(query)

    return {"message": "Pet updated"}


@pet_router.delete("/delete/pet/{pet_id}", response_model=dict, tags=["Pet"])
async def delete_pet(pet_id: str, response: Response):
    response.status_code = status.HTTP_200_OK
    exist = pet_model.select().filter_by(id=pet_id)
    pet_exist = await database.fetch_one(exist)

    if not pet_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")

    query = pet_model.delete().where(pet_model.id == pet_id)
    await database.execute(query)

    return {"message": "Pet deleted"}
