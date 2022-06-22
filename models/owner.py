from sqlalchemy import Table, Column, String, LargeBinary, Integer, ForeignKey
from db.config import meta

owner = Table(
    'owners',
    meta,
    Column('owner_id', String(256), primary_key=True),
    Column('full_name', String(256),),
    Column('email', String(256), unique=True),
    Column('phone', String(256)),
    Column('address', String(256)),
    Column('password', LargeBinary(256)),
)

pet = Table(
    'pets',
    meta,
    Column('id', String(256), primary_key=True),
    Column('name', String(256)),
    Column('breed', String(256)),
    Column('age',  Integer,),
    Column('owner_id', String(256), ForeignKey('owners.owner_id')),
)
