from fastapi import APIRouter,Response,status
from config.db import conn
from models.user import users
from schemas.User import User
from cryptography.fernet import Fernet
from sqlalchemy import select
from starlette.status import HTTP_204_NO_CONTENT



user = APIRouter()
key = Fernet.generate_key()
f = Fernet(key)

@user.get('/users',tags=["users"])
def get_user():
    l = conn.execute(users.select()).fetchall()
    d = {}
    for index,x in enumerate(l):
        x = x._asdict()
        d[index]=x
    return d


@user.post('/users',tags=["users"])
async def create_user(user: User):
    new_user = {"name":user.name,"email":user.email}
    new_user["password"]= f.encrypt(user.password.encode("utf-8"))
    r = conn.execute(users.insert().values(new_user))
    conn.commit() 
    lrid = r.lastrowid
    stmt = conn.execute(select(users).where(users.c.id == lrid)).fetchone()
    return stmt._asdict()

@user.get('/users/{id}',tags=["users"])
def read_user(id:str):
    return (conn.execute(select(users).where(users.c.id == id)).fetchone())._asdict()
    

@user.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT,tags=["users"])
def delete_user(id: str):
    conn.execute(users.delete().where(users.c.id == id))
    conn.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)

@user.put("/users/{id}",response_model=User,tags=["users"])
def update_user(id:str,user:User):
    conn.execute(users.update().values(name = user.name, email=user.email,password = f.encrypt(user.password.encode("utf-8"))).where(users.c.id == id))
    conn.commit()
    return (conn.execute(select(users).where(users.c.id == id)).fetchone())._asdict()