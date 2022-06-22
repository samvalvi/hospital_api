from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette import status

from db.config import database
from routes.pet_routes import pet_router
from routes.owner_routes import owner_router
from dotenv import load_dotenv
from os import getenv
from db.config import meta, engine


meta.create_all(bind=engine)

load_dotenv(getenv("ENV_FILE"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[getenv("CORS_ORIGIN_WHITELIST")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prefix="/owner", router=owner_router)
app.include_router(prefix="/pet", router=pet_router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
def get_root():
    return {"message": "Hsopital api", "version": "1.0.0", "status": {status.HTTP_200_OK}}