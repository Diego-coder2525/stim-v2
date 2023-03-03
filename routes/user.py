from fastapi import APIRouter, Response, status, Request, Depends
from fastapi.responses import HTMLResponse
from config.db import SessionLocal
from schemas.User import User
from cryptography.fernet import Fernet
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT
from fastapi.templating import Jinja2Templates
from models.user import User as UserModel

templates = Jinja2Templates(directory="templates")
user = APIRouter()
key = Fernet.generate_key()
f = Fernet(key)


# Middleware para crear una nueva sesión de BD para cada solicitud
def get_db(request: Request):
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
async def get_user(db: Session =Depends(get_db)):
    l = db.execute(UserModel.__table__.select()).fetchall()
    d = {}
    for index,x in enumerate(l):
        x = x._asdict()
        d[index]=x
    return d


#Crear usuario prototipo
@user.post('/users',tags=["users"])
async def create_user(user: User, db: Session=Depends(get_db)):
    new_user = {"name":user.name,"email":user.email}
    new_user["password"]= f.encrypt(user.password.encode("utf-8"))
    r = db.execute(UserModel.__table__.insert().values(new_user))
    db.commit() 
    lrid = r.lastrowid
    stmt = db.execute(UserModel.__table__.select().where(UserModel.__table__.c.id == lrid)).fetchone()
    return stmt._asdict()


#Obtener usuario prototipo por id
@user.get('/users/{id}',tags=["users"])
async def read_user(id:str, db: Session=Depends(get_db)):
    return (db.execute(UserModel.__table__.select().where(UserModel.__table__.c.id == id)).fetchone())._asdict()
    
#Eliminar usuario prototipo por id
@user.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT,tags=["users"])
async def delete_user(id: str, db: Session=Depends(get_db)):
    db.execute(UserModel.__table__.delete().where(UserModel.__table__.c.id == id))
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)


#Actualizar usuario por id
@user.put("/users/{id}", response_model=User, tags=["users"])
async def update_user(id:str,user:User, db: Session=Depends(get_db)):
    db.execute(UserModel.__table__.update().values(name=user.name, email=user.email, password=f.encrypt(user.password.encode("utf-8"))).where(UserModel.__table__.c.id == id))
    db.commit()
    updated_user = (db.execute(UserModel.__table__.select().where(UserModel.__table__.c.id == id)).fetchone())._asdict()
    return updated_user
