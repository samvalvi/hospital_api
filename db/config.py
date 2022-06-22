from databases import Database
from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv
from os import getenv


load_dotenv(getenv('ENV_PATH'))

database = Database(getenv('DATABASE_URL'), max_size=25)

meta = MetaData()

engine = create_engine(getenv('DATABASE_URL'), future=True)


