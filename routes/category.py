from fastapi import APIRouter, Response, status, Request, Depends
from fastapi.responses import HTMLResponse
from config.db import SessionLocal
from schemas.Category import Category
from cryptography.fernet import Fernet
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT
from fastapi.templating import Jinja2Templates
from models.models import Category as CategoryModel
from sqlalchemy import text

templates = Jinja2Templates(directory="templates")
category = APIRouter()
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
@category.get("/pruebaC", response_class=HTMLResponse)
async def obtener_datos(request: Request):
    datos = {"mensaje": "¡Hola, mundo!"}
    return templates.TemplateResponse("prueba.html", {"request": request, "datos": datos})


#Recibir datos del front por id y solicitud post
@category.post("/procesar_datosC")
async def procesar_datos(request: Request):
    data = await request.form()
    nombre = data["nombre"]
    email = data["email"]
    
    return {"mensaje": f"Datos recibidos correctamente: {nombre} y {email}"}


#Leer de la base de datos
@category.get('/categories',tags=["categories"])
async def get_category(db: Session =Depends(get_db)):
    l = db.execute(CategoryModel.__table__.select()).fetchall()
    d = {}
    for index,x in enumerate(l):
        x = x._asdict()
        d[index]=x
    return d


#Crear categoria prototipo
@category.post('/categories', tags=["categories"], status_code=201)
async def create_category(category: Category, db: Session = Depends(get_db)):
    new_category = {"name": category.name}
    result = db.execute(CategoryModel.__table__.insert().values(new_category))
    if db.query(CategoryModel).count() == 0:
        db.execute(text("ALTER TABLE categories AUTO_INCREMENT = 1"))
    db.commit()
    category_id = result.lastrowid
    return {"category_id": category_id, "url": f"/categories/{category_id}"}


#Obtener categoria prototipo por id
@category.get('/categories/{id}',tags=["categories"])
async def read_category(id:int, db: Session=Depends(get_db)):
    return (db.execute(CategoryModel.__table__.select().where(CategoryModel.__table__.c.id == id)).fetchone())._asdict()
    
#Eliminar categoria prototipo por id
@category.delete('/categories/{id}', status_code=status.HTTP_204_NO_CONTENT,tags=["categories"])
async def delete_category(id: int, db: Session=Depends(get_db)):
    db.execute(CategoryModel.__table__.delete().where(CategoryModel.__table__.c.id == id))
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)


#Actualizar categoria por id
@category.put("/categories/{id}", response_model=Category, tags=["categories"])
async def update_category(id:str,category:Category, db: Session=Depends(get_db)):
    db.execute(CategoryModel.__table__.update().values(name=category.name).where(CategoryModel.__table__.c.id == id))
    db.commit()
    updated_category = (db.execute(CategoryModel.__table__.select().where(CategoryModel.__table__.c.id == id)).fetchone())._asdict()
    return updated_category
