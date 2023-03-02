from fastapi import APIRouter,Response,status,Request
from fastapi.responses import HTMLResponse
from config.db import conn
from models.user import users
from schemas.User import User
from cryptography.fernet import Fernet
from sqlalchemy import select
from starlette.status import HTTP_204_NO_CONTENT
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")
user = APIRouter()
key = Fernet.generate_key()
f = Fernet(key)

#Enviar datos al front
@user.get("/prueba", response_class=HTMLResponse)
async def obtener_datos(request: Request):
    datos = {"mensaje": "¡Hola, mundo!"}
    return templates.TemplateResponse("prueba.html", {"request": request, "datos": datos})

#Recibir datos del front por id y solicitud post
@user.post("/procesar_datos")
async def procesar_datos(request: Request):
    data = await request.form()
    nombre = data["nombre"]
    email = data["email"]
    
    return {"mensaje": f"Datos recibidos correctamente: {nombre} y {email}"}


#Leer de la base de datos
@user.get('/users',tags=["users"])
async def get_user():
    l = conn.execute(users.select()).fetchall()
    d = {}
    for index,x in enumerate(l):
        x = x._asdict()
        d[index]=x
    return d

#Crear usuario prototipo
@user.post('/users',tags=["users"])
async def create_user(user: User):
    new_user = {"name":user.name,"email":user.email}
    new_user["password"]= f.encrypt(user.password.encode("utf-8"))
    r = conn.execute(users.insert().values(new_user))
    conn.commit() 
    lrid = r.lastrowid
    stmt = conn.execute(select(users).where(users.c.id == lrid)).fetchone()
    return stmt._asdict()

#Obtener usuario prototipo por id
@user.get('/users/{id}',tags=["users"])
async def read_user(id:str):
    return (conn.execute(select(users).where(users.c.id == id)).fetchone())._asdict()
    
#Eliminar usuario prototipo por id
@user.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT,tags=["users"])
async def delete_user(id: str):
    conn.execute(users.delete().where(users.c.id == id))
    conn.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)


#Actualizar usuario por id
@user.put("/users/{id}",response_model=User,tags=["users"])
async def update_user(id:str,user:User):
    conn.execute(users.update().values(name = user.name, email=user.email,password = f.encrypt(user.password.encode("utf-8"))).where(users.c.id == id))
    conn.commit()
    return (conn.execute(select(users).where(users.c.id == id)).fetchone())._asdict()