from fastapi import APIRouter, Response, status, Request, Depends
from fastapi.responses import HTMLResponse
from config.db import SessionLocal
from schemas.Game import Game
from cryptography.fernet import Fernet
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT
from fastapi.templating import Jinja2Templates
from models.models import Game as GameModel
from sqlalchemy import text
templates = Jinja2Templates(directory="templates")
game = APIRouter()
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
@game.get("/pruebaG", response_class=HTMLResponse)
async def obtener_datos(request: Request):
    datos = {"mensaje": "¡Hola, mundo!"}
    return templates.TemplateResponse("prueba.html", {"request": request, "datos": datos})


#Recibir datos del front por id y solicitud post
@game.post("/procesar_datosG")
async def procesar_datos(request: Request):
    data = await request.form()
    nombre = data["nombre"]
    email = data["email"]
    
    return {"mensaje": f"Datos recibidos correctamente: {nombre} y {email}"}


#Leer de la base de datos
@game.get('/games',tags=["games"])
async def get_game(db: Session =Depends(get_db)):
    l = db.execute(GameModel.__table__.select()).fetchall()
    d = {}
    for index,x in enumerate(l):
        x = x._asdict()
        d[index]=x
    return d


#Crear game prototipo
@game.post('/games',tags=["games"])
async def create_game(game: Game, db: Session=Depends(get_db)):
    new_game = {"name":game.name,"description":game.description,"price":game.price}
    r = db.execute(GameModel.__table__.insert().values(new_game))
    if db.query(GameModel).count() == 0:
        db.execute(text("ALTER TABLE  AUTO_INCREMENT = 1"))
    db.commit() 
    lrid = r.lastrowid
    stmt = db.execute(GameModel.__table__.select().where(GameModel.__table__.c.id == lrid)).fetchone()
    return stmt._asdict()


#Obtener game prototipo por id
@game.get('/games/{id}',tags=["games"])
async def read_game(id:str, db: Session=Depends(get_db)):
    return (db.execute(GameModel.__table__.select().where(GameModel.__table__.c.id == id)).fetchone())._asdict()
    
#Eliminar game prototipo por id
@game.delete('/games/{id}', status_code=status.HTTP_204_NO_CONTENT,tags=["games"])
async def delete_game(id: str, db: Session=Depends(get_db)):
    db.execute(GameModel.__table__.delete().where(GameModel.__table__.c.id == id))
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)


#Actualizar game por id
@game.put("/games/{id}", response_model=Game, tags=["games"])
async def update_game(id:str,game:Game, db: Session=Depends(get_db)):
    db.execute(GameModel.__table__.update().values(name=game.name, description=game.description, price=game.price).where(GameModel.__table__.c.id == id))
    db.commit()
    updated_game = (db.execute(GameModel.__table__.select().where(GameModel.__table__.c.id == id)).fetchone())._asdict()
    return updated_game
