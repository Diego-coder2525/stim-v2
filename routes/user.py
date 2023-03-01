from fastapi import APIRouter
from config.db import conn
from models.user import users
from schemas.User import User
from cryptography.fernet import Fernet
user = APIRouter()
key = Fernet.generate_key()
f = Fernet(key)
@user.get('/users')
def get_user():
    return "h"
@user.post('/users')
def create_user(user: User):
    new_user = {"name":user.name,"email":user.email}
    new_user["password"]= f.encrypt(user.password.encode("utf-8"))
    r = conn.execute(users.insert().values(new_user))
    
    conn.commit() # <-- subir la transaccion actual
    #print(r.lastrowid) 
    return "Recibido"

@user.get('users/{id}')
def read_user(id:str):
    return "h"
    
@user.get('/')
def get_user():
    return "h"